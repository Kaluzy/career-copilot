"""
Lever ATS connector.
Public API: https://api.lever.co/v0/postings/{slug}?mode=json
No auth required for public postings.
"""
import httpx
from datetime import datetime, timezone
from ingestion.normalizer import normalize_job


LEVER_URL = "https://api.lever.co/v0/postings/{slug}?mode=json&limit=250"
HEADERS = {"User-Agent": "CareerCopilot/1.0 (personal job tracker)"}


async def fetch_jobs(company: dict) -> list[dict]:
    """
    Fetch all jobs from a Lever company board.
    company: row from companies table with ats_slug set.
    Returns list of normalized job dicts ready to upsert.
    """
    slug = company.get("ats_slug")
    if not slug:
        print(f"[lever] Skipping {company['name']} — no ats_slug")
        return []

    url = LEVER_URL.format(slug=slug)
    jobs = []

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            raw_jobs = resp.json()
        except Exception as e:
            print(f"[lever] Error fetching {company['name']}: {e}")
            return []

        if not isinstance(raw_jobs, list):
            raw_jobs = raw_jobs.get("postings", [])

        print(f"[lever] {company['name']}: {len(raw_jobs)} jobs found")

        for raw in raw_jobs:
            job_id = raw.get("id", "")
            title = raw.get("text", "")

            # Location
            cats = raw.get("categories", {})
            location = cats.get("location", "") or raw.get("workplaceType", "")

            # Apply URL
            apply_url = raw.get("applyUrl", "") or raw.get("hostedUrl", "")

            # Posted date (Lever uses epoch ms)
            posted_at = None
            created_ms = raw.get("createdAt")
            if created_ms:
                try:
                    posted_at = datetime.fromtimestamp(
                        created_ms / 1000, tz=timezone.utc
                    ).date().isoformat()
                except Exception:
                    pass

            # Description — Lever includes it in the list response
            desc_parts = []
            for section in raw.get("descriptionBody", {}).get("descriptionBodyParts", []):
                desc_parts.append(section.get("descriptionBodyText", ""))
            description_raw = "\n\n".join(desc_parts) or raw.get("description", "")

            raw_normalized = {
                "job_id": job_id,
                "title": title,
                "location": location,
                "apply_url": apply_url,
                "posted_at": posted_at,
                "description_raw": description_raw,
            }

            normalized = normalize_job(
                raw=raw_normalized,
                company_id=company["id"],
                company_slug=company["slug"],
                ats_type="lever",
            )
            jobs.append(normalized)

    return jobs

"""
Ashby ATS connector.
Public API: https://jobs.ashbyhq.com/{slug}/non-applied/job-board-api
No auth required. Returns JSON with all postings + descriptions included.
"""
import httpx
from datetime import datetime
from ingestion.normalizer import normalize_job

ASHBY_URL = "https://jobs.ashbyhq.com/{slug}/non-applied/job-board-api"
HEADERS = {"User-Agent": "CareerCopilot/1.0 (personal job tracker)"}


async def fetch_jobs(company: dict) -> list[dict]:
    slug = company.get("ats_slug")
    if not slug:
        print(f"[ashby] Skipping {company['name']} — no ats_slug")
        return []

    url = ASHBY_URL.format(slug=slug)
    jobs = []

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[ashby] Error fetching {company['name']}: {e}")
            return []

        raw_jobs = data.get("jobPostings", [])
        print(f"[ashby] {company['name']}: {len(raw_jobs)} jobs found")

        for raw in raw_jobs:
            job_id   = raw.get("id", "")
            title    = raw.get("title", "")
            location = raw.get("locationName", "") or raw.get("location", "")
            apply_url = f"https://jobs.ashbyhq.com/{slug}/{job_id}"

            # Posted date
            posted_at = None
            created = raw.get("publishedAt") or raw.get("createdAt", "")
            if created:
                try:
                    posted_at = datetime.fromisoformat(
                        created.replace("Z", "+00:00")
                    ).date().isoformat()
                except Exception:
                    pass

            # Description included in Ashby list response
            desc_parts = []
            for section in raw.get("descriptionSections", []):
                desc_parts.append(section.get("content", ""))
            description_raw = "\n\n".join(desc_parts) or raw.get("description", "")

            normalized = normalize_job(
                raw={
                    "job_id": job_id,
                    "title": title,
                    "location": location,
                    "apply_url": apply_url,
                    "posted_at": posted_at,
                    "description_raw": description_raw,
                },
                company_id=company["id"],
                company_slug=company["slug"],
                ats_type="ashby",
            )
            jobs.append(normalized)

    return jobs

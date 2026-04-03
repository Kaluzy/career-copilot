"""
Ashby ATS connector.
Public API: https://api.ashbyhq.com/posting-api/job-board/{slug}
No auth required. Returns JSON with all postings + descriptions included.
"""
import httpx
from datetime import datetime
from ingestion.normalizer import normalize_job

ASHBY_URL = "https://api.ashbyhq.com/posting-api/job-board/{slug}"
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

        raw_jobs = data.get("jobs", [])
        print(f"[ashby] {company['name']}: {len(raw_jobs)} jobs found")

        for raw in raw_jobs:
            job_id = raw.get("id", "")
            title  = raw.get("title", "")

            # Location — Ashby provides structured address + workplaceType
            loc_parts = []
            address = raw.get("address") or {}
            city    = address.get("city", "")
            state   = address.get("state", "")
            country = address.get("country", "")
            if city:    loc_parts.append(city)
            if state:   loc_parts.append(state)
            if country and country != "United States": loc_parts.append(country)
            location = ", ".join(loc_parts)

            workplace = raw.get("workplaceType", "")  # "Remote", "OnSite", "Hybrid"
            if workplace == "Remote" and not location:
                location = "Remote"
            elif workplace == "Remote":
                location = f"Remote - {location}"
            elif workplace == "Hybrid":
                location = f"Hybrid - {location}" if location else "Hybrid"

            apply_url = raw.get("jobUrl", f"https://jobs.ashbyhq.com/{slug}/{job_id}")

            # Posted date
            posted_at = None
            created = raw.get("publishedAt") or raw.get("updatedAt", "")
            if created:
                try:
                    posted_at = datetime.fromisoformat(
                        created.replace("Z", "+00:00")
                    ).date().isoformat()
                except Exception:
                    pass

            # Description — Ashby includes both HTML and plain text
            description_raw = raw.get("descriptionHtml") or raw.get("descriptionPlain", "")

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

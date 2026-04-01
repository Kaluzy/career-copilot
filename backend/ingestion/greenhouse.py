"""
Greenhouse ATS connector.
Public API: https://boards-api.greenhouse.io/v1/boards/{slug}/jobs
No auth required for public job boards.
"""
import httpx
from datetime import datetime
from ingestion.normalizer import normalize_job


GREENHOUSE_LIST_URL = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
GREENHOUSE_JOB_URL  = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs/{job_id}"
HEADERS = {"User-Agent": "CareerCopilot/1.0 (personal job tracker)"}


async def fetch_jobs(company: dict) -> list[dict]:
    """
    Fetch all jobs from a Greenhouse company board.
    company: row from companies table with ats_slug set.
    Returns list of normalized job dicts ready to upsert.
    """
    slug = company.get("ats_slug")
    if not slug:
        print(f"[greenhouse] Skipping {company['name']} — no ats_slug")
        return []

    url = GREENHOUSE_LIST_URL.format(slug=slug)
    jobs = []

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[greenhouse] Error fetching {company['name']}: {e}")
            return []

        raw_jobs = data.get("jobs", [])
        print(f"[greenhouse] {company['name']}: {len(raw_jobs)} jobs found")

        for raw in raw_jobs:
            job_id = str(raw.get("id", ""))
            title = raw.get("title", "")
            location = raw.get("location", {}).get("name", "")
            apply_url = raw.get("absolute_url", "")
            updated_at = raw.get("updated_at", "")

            # Parse posted date
            posted_at = None
            if updated_at:
                try:
                    posted_at = datetime.fromisoformat(
                        updated_at.replace("Z", "+00:00")
                    ).date().isoformat()
                except Exception:
                    pass

            # Fetch full description (separate API call per job)
            description_raw = ""
            try:
                detail_url = GREENHOUSE_JOB_URL.format(slug=slug, job_id=job_id)
                detail_resp = await client.get(detail_url)
                if detail_resp.status_code == 200:
                    detail = detail_resp.json()
                    description_raw = detail.get("content", "")
            except Exception:
                pass  # description is nice to have, not required

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
                ats_type="greenhouse",
            )
            jobs.append(normalized)

    return jobs

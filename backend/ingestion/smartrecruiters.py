"""
SmartRecruiters ATS connector.
Public API: https://api.smartrecruiters.com/v1/companies/{id}/postings
No auth required for public job postings.
Pagination: offset + limit params, total in response.
"""
import httpx
from datetime import datetime
from ingestion.normalizer import normalize_job

SR_LIST_URL  = "https://api.smartrecruiters.com/v1/companies/{id}/postings"
SR_DETAIL_URL = "https://api.smartrecruiters.com/v1/companies/{id}/postings/{job_id}"
HEADERS = {"User-Agent": "CareerCopilot/1.0 (personal job tracker)"}
PAGE_LIMIT = 100


async def fetch_jobs(company: dict) -> list[dict]:
    slug = company.get("ats_slug")
    if not slug:
        print(f"[smartrecruiters] Skipping {company['name']} - no ats_slug")
        return []

    jobs = []
    offset = 0

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        while True:
            url = SR_LIST_URL.format(id=slug)
            try:
                resp = await client.get(url, params={"limit": PAGE_LIMIT, "offset": offset})
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"[smartrecruiters] Error fetching {company['name']}: {e}")
                break

            raw_jobs = data.get("content", [])
            total = data.get("totalFound", 0)

            for raw in raw_jobs:
                job_id = raw.get("id", "")
                title  = raw.get("name", "") or raw.get("title", "")

                # Location
                loc_obj  = raw.get("location", {}) or {}
                city     = loc_obj.get("city", "")
                country  = loc_obj.get("country", "")
                remote   = loc_obj.get("remote", False)
                location = f"{city}, {country}".strip(", ") if city or country else ""
                if remote:
                    location = ("Remote - " + location).strip(" -") if location else "Remote"

                apply_url = f"https://jobs.smartrecruiters.com/{slug}/{job_id}"

                # Posted date
                posted_at = None
                created = raw.get("releasedDate") or raw.get("createdon", "")
                if created:
                    try:
                        posted_at = datetime.fromisoformat(
                            created.replace("Z", "+00:00")
                        ).date().isoformat()
                    except Exception:
                        pass

                # Fetch description separately (not included in list)
                description_raw = ""
                try:
                    det = await client.get(SR_DETAIL_URL.format(id=slug, job_id=job_id))
                    if det.status_code == 200:
                        det_data = det.json()
                        sections = det_data.get("jobAd", {}).get("sections", {})
                        parts = []
                        for key in ("companyDescription", "jobDescription", "qualifications", "additionalInformation"):
                            content = sections.get(key, {}).get("text", "")
                            if content:
                                parts.append(content)
                        description_raw = "\n\n".join(parts)
                except Exception:
                    pass

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
                    ats_type="smartrecruiters",
                )
                jobs.append(normalized)

            offset += len(raw_jobs)
            if offset >= total or not raw_jobs:
                break

    print(f"[smartrecruiters] {company['name']}: {len(jobs)} jobs found")
    return jobs

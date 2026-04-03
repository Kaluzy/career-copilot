"""
Adzuna job search connector.
API docs: https://developer.adzuna.com/
Free tier: 250 req/month per app. Register at https://developer.adzuna.com/signup

Required env vars:
  ADZUNA_APP_ID  — from developer portal
  ADZUNA_API_KEY — from developer portal

Unlike other connectors, Adzuna is a search engine, not a company ATS.
We run keyword searches for IT roles in the US and ingest matching results.
"""
import httpx
import os
from datetime import datetime
from ingestion.normalizer import normalize_job

ADZUNA_URL = "https://api.adzuna.com/v1/api/jobs/us/search/{page}"
HEADERS = {"User-Agent": "CareerCopilot/1.0 (personal job tracker)"}

# Search queries targeting IT roles we care about
SEARCH_QUERIES = [
    "endpoint management engineer",
    "endpoint administrator intune sccm",
    "digital workplace engineer",
    "MDM engineer intune jamf",
    "desktop engineer deployment",
    "systems administrator windows",
    "IT operations engineer remote",
]

RESULTS_PER_PAGE = 50
MAX_PAGES = 2  # 100 results per query, keeps request count low


async def fetch_jobs(company: dict) -> list[dict]:
    """
    For Adzuna, 'company' is a synthetic sentinel row (name='Adzuna Search').
    We ignore company fields and run keyword searches instead.
    """
    app_id  = os.getenv("ADZUNA_APP_ID")
    api_key = os.getenv("ADZUNA_API_KEY")

    if not app_id or not api_key:
        print("[adzuna] Skipping - ADZUNA_APP_ID / ADZUNA_API_KEY not set")
        return []

    all_jobs: list[dict] = []
    seen_ids: set[str] = set()

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        for query in SEARCH_QUERIES:
            for page in range(1, MAX_PAGES + 1):
                params = {
                    "app_id":        app_id,
                    "app_key":       api_key,
                    "results_per_page": RESULTS_PER_PAGE,
                    "what":          query,
                    "content-type":  "application/json",
                    "max_days_old":  30,  # only fresh jobs
                }
                url = ADZUNA_URL.format(page=page)
                try:
                    resp = await client.get(url, params=params)
                    resp.raise_for_status()
                    data = resp.json()
                except Exception as e:
                    print(f"[adzuna] Error on query '{query}' page {page}: {e}")
                    break

                results = data.get("results", [])
                if not results:
                    break

                for raw in results:
                    job_id = str(raw.get("id", ""))
                    if job_id in seen_ids:
                        continue
                    seen_ids.add(job_id)

                    title       = raw.get("title", "")
                    location    = raw.get("location", {}).get("display_name", "")
                    apply_url   = raw.get("redirect_url", "")
                    description_raw = raw.get("description", "")

                    # Company name from listing (not from our registry)
                    raw_company_name = raw.get("company", {}).get("display_name", "Unknown")

                    posted_at = None
                    created = raw.get("created", "")
                    if created:
                        try:
                            posted_at = datetime.fromisoformat(
                                created.replace("Z", "+00:00")
                            ).date().isoformat()
                        except Exception:
                            pass

                    # Salary (Adzuna provides min/max directly)
                    salary_min = raw.get("salary_min")
                    salary_max = raw.get("salary_max")
                    if salary_min:
                        salary_min = int(salary_min)
                    if salary_max:
                        salary_max = int(salary_max)

                    normalized = normalize_job(
                        raw={
                            "job_id":          job_id,
                            "title":           title,
                            "location":        location,
                            "apply_url":       apply_url,
                            "posted_at":       posted_at,
                            "description_raw": description_raw,
                            "salary_min":      salary_min,
                            "salary_max":      salary_max,
                        },
                        company_id=company["id"],   # sentinel Adzuna row id
                        company_slug="adzuna",
                        ats_type="adzuna",
                    )
                    # Overwrite title to include source company name so UI shows it
                    normalized["title"] = f"{title} @ {raw_company_name}"
                    all_jobs.append(normalized)

    print(f"[adzuna] Total: {len(all_jobs)} jobs fetched across {len(SEARCH_QUERIES)} queries")
    return all_jobs

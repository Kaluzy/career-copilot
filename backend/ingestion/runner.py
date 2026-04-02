"""
Ingestion runner — coordinates all connectors and upserts to Supabase.
Called by the scheduler (daily) or manually via API.
"""
import asyncio
from database import get_db
from ingestion import greenhouse, lever


CONNECTOR_MAP = {
    "greenhouse": greenhouse.fetch_jobs,
    "lever":      lever.fetch_jobs,
}


async def run_ingestion(company_slug: str | None = None) -> dict:
    """
    Run ingestion for all active companies (or one specific company).
    Returns summary stats.
    """
    db = get_db()
    stats = {"companies_processed": 0, "jobs_ingested": 0, "jobs_skipped": 0, "errors": []}

    # Fetch companies from DB
    query = db.table("companies").select("*").eq("active", True)
    if company_slug:
        query = query.eq("slug", company_slug)

    result = query.execute()
    companies = result.data or []

    # Only process companies with a supported connector
    supported = [c for c in companies if c.get("ats_type") in CONNECTOR_MAP]

    print(f"[runner] Processing {len(supported)} companies...")

    for company in supported:
        ats_type = company["ats_type"]
        connector = CONNECTOR_MAP[ats_type]

        try:
            jobs = await connector(company)
            stats["companies_processed"] += 1

            if not jobs:
                continue

            # Upsert jobs — skip if source_id already exists (dedup)
            for job in jobs:
                try:
                    db.table("jobs").upsert(
                        job,
                        on_conflict="source_id",
                        ignore_duplicates=True
                    ).execute()
                    stats["jobs_ingested"] += 1
                except Exception as e:
                    stats["jobs_skipped"] += 1
                    print(f"[runner] Skip job ({job.get('title')}): {e}")

            print(f"[runner] OK {company['name']}: {len(jobs)} jobs processed")

        except Exception as e:
            stats["errors"].append({"company": company["name"], "error": str(e)})
            print(f"[runner] FAIL {company['name']}: {e}")

        # Small delay between companies to be polite
        await asyncio.sleep(1)

    print(f"[runner] Done ingesting. {stats}")

    # Auto-score new jobs for every user that has a profile
    db2 = get_db()
    profiles = db2.table("candidate_profile").select("user_id").execute().data or []
    stats["scored"] = 0
    for p in profiles:
        try:
            score_stats = await run_scoring_for_user(p["user_id"])
            stats["scored"] += score_stats.get("scored", 0)
        except Exception as e:
            print(f"[runner] Scoring failed for user {p['user_id'][:8]}: {e}")

    print(f"[runner] Done scoring. Total scored: {stats['scored']}")
    return stats


async def run_scoring_for_user(user_id: str) -> dict:
    """
    Score all unscored jobs for a specific user.
    Imports scorer inline to avoid circular imports.
    """
    from scoring.scorer import score_job
    db = get_db()

    # Get user's profile
    profile_result = db.table("candidate_profile").select("*").eq("user_id", user_id).single().execute()
    profile = profile_result.data
    if not profile:
        return {"error": "No candidate profile found for user"}

    # Get all jobs that haven't been scored for this user yet
    all_jobs = db.table("jobs").select("*").eq("status", "new").execute().data or []
    scored_ids = {
        r["job_id"]
        for r in (db.table("fit_scores").select("job_id").eq("user_id", user_id).execute().data or [])
    }
    unscored = [j for j in all_jobs if j["id"] not in scored_ids]

    print(f"[scorer] Scoring {len(unscored)} jobs for user {user_id[:8]}...")
    scored = 0

    for job in unscored:
        company = db.table("companies").select("*").eq("id", job["company_id"]).single().execute().data or {}
        fit = score_job(job, profile, company)
        fit["user_id"] = user_id
        fit["job_id"] = job["id"]

        db.table("fit_scores").upsert(fit, on_conflict="job_id,user_id").execute()

        # Update job status to 'scored'
        db.table("jobs").update({"status": "scored"}).eq("id", job["id"]).execute()
        scored += 1

    return {"scored": scored}

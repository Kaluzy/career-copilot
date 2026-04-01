"""
Jobs router — read/filter scored job listings.
GET  /api/jobs          — paginated list with tier/category/remote filters
GET  /api/jobs/{job_id} — single job with full score breakdown
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from database import get_db

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("")
async def list_jobs(
    user_id: str = Query(..., description="Auth user UUID"),
    tier: Optional[str] = Query(None, description="strong_fit|good_fit|stretch|pass"),
    category: Optional[str] = Query(None, description="role_category filter"),
    remote: Optional[bool] = Query(None, description="Filter remote-only"),
    min_score: Optional[int] = Query(None, ge=0, le=100),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Return jobs with their fit scores for the given user."""
    db = get_db()

    # Build a joined query: jobs + fit_scores for this user
    query = (
        db.table("fit_scores")
        .select("*, jobs(*)")
        .eq("user_id", user_id)
    )

    if tier:
        query = query.eq("tier", tier)
    if min_score is not None:
        query = query.gte("composite", min_score)

    query = query.order("composite", desc=True).range(offset, offset + limit - 1)
    result = query.execute()
    rows = result.data or []

    # Post-filter by category / remote (stored on the job, not fit_score)
    if category or remote is not None:
        filtered = []
        for row in rows:
            job = row.get("jobs") or {}
            if category and job.get("role_category") != category:
                continue
            if remote is True and not job.get("remote"):
                continue
            filtered.append(row)
        rows = filtered

    return {"jobs": rows, "count": len(rows), "offset": offset}


@router.get("/{job_id}")
async def get_job(job_id: str, user_id: str = Query(...)):
    """Single job with fit score breakdown."""
    db = get_db()

    job_result = db.table("jobs").select("*, companies(*)").eq("id", job_id).single().execute()
    if not job_result.data:
        raise HTTPException(status_code=404, detail="Job not found")

    score_result = (
        db.table("fit_scores")
        .select("*")
        .eq("job_id", job_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    return {
        "job": job_result.data,
        "fit_score": score_result.data,
    }

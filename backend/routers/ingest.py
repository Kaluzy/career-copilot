"""
Ingest router — manually trigger ingestion and scoring pipelines.
POST /api/ingest              — run full ingestion (all companies or one)
POST /api/ingest/score        — score all unscored jobs for a user
GET  /api/ingest/status       — last run stats (stored in Supabase settings table)
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from database import get_db

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


class IngestRequest(BaseModel):
    company_slug: Optional[str] = None   # Omit to run all companies


class ScoreRequest(BaseModel):
    user_id: str


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("")
async def trigger_ingestion(body: IngestRequest, background_tasks: BackgroundTasks):
    """
    Kick off job ingestion in the background.
    Returns immediately; check /api/ingest/status for results.
    """
    from ingestion.runner import run_ingestion

    async def _run():
        try:
            stats = await run_ingestion(company_slug=body.company_slug)
        except Exception as e:
            stats = {"error": str(e)}
            print(f"[ingest] background task failed: {e}")
        try:
            db = get_db()
            db.table("system_settings").upsert(
                {"key": "last_ingest_stats", "value": stats},
                on_conflict="key"
            ).execute()
        except Exception as e:
            print(f"[ingest] failed to save stats: {e}")

    background_tasks.add_task(_run)
    scope = body.company_slug or "all companies"
    return {"message": f"Ingestion started for {scope}"}


@router.post("/score")
async def trigger_scoring(body: ScoreRequest, background_tasks: BackgroundTasks):
    """Score all unscored jobs for the given user in the background."""
    from ingestion.runner import run_scoring_for_user

    async def _run():
        await run_scoring_for_user(body.user_id)

    background_tasks.add_task(_run)
    return {"message": f"Scoring started for user {body.user_id[:8]}..."}


@router.get("/status")
async def ingest_status():
    """Return stats from the last ingestion run."""
    db = get_db()
    result = (
        db.table("system_settings")
        .select("value, updated_at")
        .eq("key", "last_ingest_stats")
        .maybe_single()
        .execute()
    )
    if not result or not result.data:
        return {"status": "no_runs_yet"}
    return result.data


@router.get("/companies")
async def list_companies(
    active_only: bool = Query(True),
    ats_type: Optional[str] = Query(None),
):
    """Return companies in the registry."""
    db = get_db()
    query = db.table("companies").select("id, name, slug, ats_type, ats_slug, active, user_status")
    if active_only:
        query = query.eq("active", True)
    if ats_type:
        query = query.eq("ats_type", ats_type)
    result = query.order("name").execute()
    return {"companies": result.data or []}

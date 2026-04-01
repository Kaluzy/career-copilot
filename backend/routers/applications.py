"""
Applications router — track where you've applied and outcomes.
POST   /api/applications           — log a new application
GET    /api/applications           — list all apps for user
PATCH  /api/applications/{app_id}  — update status / notes / outcome
DELETE /api/applications/{app_id}  — remove (rare, but useful)
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_db

router = APIRouter(prefix="/api/applications", tags=["applications"])


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class ApplicationCreate(BaseModel):
    user_id: str
    job_id: str
    applied_at: Optional[date] = None
    status: str = "applied"         # applied|phone_screen|interview|offer|rejected|withdrawn
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    outcome: Optional[str] = None   # offer|rejected|withdrawn|ghosted
    outcome_at: Optional[date] = None
    offer_amount: Optional[int] = None
    rejection_reason: Optional[str] = None


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("", status_code=201)
async def create_application(body: ApplicationCreate):
    db = get_db()
    payload = body.model_dump(exclude_none=True)
    if "applied_at" not in payload:
        payload["applied_at"] = date.today().isoformat()
    else:
        payload["applied_at"] = payload["applied_at"].isoformat()

    result = db.table("applications").insert(payload).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create application")
    return result.data[0]


@router.get("")
async def list_applications(
    user_id: str = Query(...),
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    db = get_db()
    query = (
        db.table("applications")
        .select("*, jobs(title, company_id, companies(name, logo_url))")
        .eq("user_id", user_id)
        .order("applied_at", desc=True)
        .range(offset, offset + limit - 1)
    )
    if status:
        query = query.eq("status", status)

    result = query.execute()
    return {"applications": result.data or [], "offset": offset}


@router.patch("/{app_id}")
async def update_application(app_id: str, body: ApplicationUpdate):
    db = get_db()
    payload = body.model_dump(exclude_none=True)

    if "outcome_at" in payload:
        payload["outcome_at"] = payload["outcome_at"].isoformat()

    result = db.table("applications").update(payload).eq("id", app_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Application not found")
    return result.data[0]


@router.delete("/{app_id}", status_code=204)
async def delete_application(app_id: str):
    db = get_db()
    db.table("applications").delete().eq("id", app_id).execute()

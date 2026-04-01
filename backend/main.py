"""
Career Copilot — FastAPI application entry point.
Run: uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import get_settings
settings = get_settings()

from routers import jobs, applications, ingest


# ── Scheduler (APScheduler) ───────────────────────────────────────────────────
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()


async def scheduled_ingestion():
    """Daily ingestion job — runs at 6 AM UTC."""
    from ingestion.runner import run_ingestion
    print("[scheduler] Starting daily ingestion...")
    stats = await run_ingestion()
    print(f"[scheduler] Done: {stats}")


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.add_job(
        scheduled_ingestion,
        CronTrigger(hour=6, minute=0),   # 6:00 AM UTC daily
        id="daily_ingest",
        replace_existing=True,
    )
    scheduler.start()
    print("[app] Scheduler started — daily ingestion at 06:00 UTC")
    yield
    # Shutdown
    scheduler.shutdown()
    print("[app] Scheduler stopped")


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Career Copilot API",
    version="0.1.0",
    description="AI-powered job search assistant — Phase 0 MVP",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(ingest.router)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}

# Career Copilot

AI-powered job search assistant. Monitors target company job boards daily, scores every opening against your profile, and surfaces only the roles worth applying to.

**Phase 0 MVP** — ingestion + scoring pipeline, REST API, React dashboard.

---

## Architecture

```
frontend/          React + Vite + Tailwind
backend/           FastAPI (Python 3.11+)
  ├── ingestion/   ATS connectors (Greenhouse, Lever)
  ├── scoring/     Rule-based fit scoring engine
  └── routers/     REST API (jobs, applications, ingest)
db/                Supabase SQL migrations + seed data
```

**Supabase** — PostgreSQL + pgvector + Auth + RLS
**ATS connectors** — public Greenhouse/Lever APIs (no auth required)
**Fit scoring** — 7-dimension weighted score (role_fit 30%, growth 20%, skills 20%, comp 10%, remote 10%, company 5%, realism 5%)

---

## Setup

### 1. Supabase

1. Create a new Supabase project at supabase.com
2. Run migrations in order:

```sql
-- In Supabase SQL Editor:
-- Paste and run db/schema.sql
-- Then db/seed_companies.sql
-- Then db/seed_profile.sql  (edit with your real profile first)
```

3. Enable the **pgvector** extension:
   Dashboard → Database → Extensions → search `vector` → Enable

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env — fill in SUPABASE_URL and SUPABASE_SERVICE_KEY
```

**.env keys you need:**

| Key | Where to find it |
|-----|-----------------|
| `SUPABASE_URL` | Project Settings → API → Project URL |
| `SUPABASE_SERVICE_KEY` | Project Settings → API → service_role key |
| `SUPABASE_ANON_KEY` | Project Settings → API → anon/public key |
| `ANTHROPIC_API_KEY` | console.anthropic.com (optional — Phase 2) |

### 3. Run the backend

```bash
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 4. Trigger first ingestion

```bash
# Ingest all active companies
curl -X POST http://localhost:8000/api/ingest

# Or just one company
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{"company_slug": "microsoft"}'

# Score jobs for your user
curl -X POST http://localhost:8000/api/ingest/score \
  -H "Content-Type: application/json" \
  -d '{"user_id": "YOUR_SUPABASE_USER_UUID"}'

# Check ingestion status
curl http://localhost:8000/api/ingest/status
```

### 5. View scored jobs

```bash
# Top jobs for your user (strong_fit tier)
curl "http://localhost:8000/api/jobs?user_id=YOUR_UUID&tier=strong_fit"

# All jobs scoring 65+
curl "http://localhost:8000/api/jobs?user_id=YOUR_UUID&min_score=65"
```

---

## API Reference

### Jobs

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/jobs` | List scored jobs (filterable by tier, category, remote, min_score) |
| GET | `/api/jobs/{job_id}` | Single job with full score breakdown |

**Query params for GET /api/jobs:**
- `user_id` (required) — your Supabase auth UUID
- `tier` — `strong_fit` / `good_fit` / `stretch` / `pass`
- `category` — `endpoint_management` / `digital_workplace` / `systems_admin` / etc.
- `remote` — `true` / `false`
- `min_score` — integer 0–100
- `limit` / `offset` — pagination

### Applications

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/applications` | Log a new application |
| GET | `/api/applications` | List your applications |
| PATCH | `/api/applications/{id}` | Update status / outcome / notes |
| DELETE | `/api/applications/{id}` | Remove application record |

**Application statuses:** `applied` → `phone_screen` → `interview` → `offer` / `rejected` / `withdrawn`

### Ingest

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/ingest` | Trigger job ingestion (background) |
| POST | `/api/ingest/score` | Score unscored jobs for a user (background) |
| GET | `/api/ingest/status` | Stats from last ingestion run |
| GET | `/api/ingest/companies` | List companies in registry |

---

## Fit Score Tiers

| Tier | Score | Meaning |
|------|-------|---------|
| `strong_fit` | 80–100 | Apply immediately |
| `good_fit` | 65–79 | Strong candidate, worth applying |
| `stretch` | 50–64 | Possible, needs strong cover letter |
| `pass` | < 50 | Not worth the time |

---

## Roadmap

| Phase | Status | Features |
|-------|--------|---------|
| 0 | **In progress** | Ingestion, scoring, REST API |
| 1 | Planned | React dashboard, application tracker |
| 2 | Planned | Claude AI rationale, resume tailoring |
| 3 | Planned | pgvector semantic search, MCP server, CLI |

---

## Adding a New Company

1. Insert into Supabase `companies` table:

```sql
INSERT INTO companies (name, slug, website, ats_type, ats_slug, active)
VALUES ('Acme Corp', 'acme', 'https://acme.com', 'greenhouse', 'acme', true);
```

2. `ats_slug` is the slug used in the ATS URL:
   - Greenhouse: `boards-api.greenhouse.io/v1/boards/**{ats_slug}**/jobs`
   - Lever: `api.lever.co/v0/postings/**{ats_slug}**`

3. Trigger ingestion: `POST /api/ingest {"company_slug": "acme"}`

---

## Tech Stack

- **Backend:** Python 3.11, FastAPI, httpx, APScheduler, pydantic-settings
- **Database:** Supabase (PostgreSQL 15 + pgvector)
- **ATS connectors:** Greenhouse public API, Lever public API
- **Frontend (Phase 1):** React 18, Vite, Tailwind CSS
- **AI (Phase 2):** Anthropic Claude (claude-sonnet-4-6)

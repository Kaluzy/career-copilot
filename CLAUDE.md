# Career Copilot — Claude Context

## What This Is
An AI-powered job search assistant built for Kaleab Tesfaye to land IT growth roles (endpoint management, sysadmin, digital workplace, MDM). Strategic targeting tool — not a spam-apply bot. Monitors target company job boards daily, scores openings against Kaleab's profile, surfaces only roles worth his time.

## Current Status: Phase 1 — FULLY LIVE

## Live URLs
- **Frontend**: https://kaluzy.github.io/career-copilot/
- **Backend (Render)**: https://career-copilot-65h5.onrender.com
- **Supabase project**: https://yxpcsfwrijybekpcszce.supabase.co
- **GitHub repo**: https://github.com/Kaluzy/career-copilot

## Tech Stack
| Layer | Tech |
|---|---|
| Backend | Python 3.11 + FastAPI — deployed on Render |
| Database | Supabase (PostgreSQL + pgvector + Auth) |
| ATS connectors | Greenhouse + Lever public APIs |
| Frontend | Single-page HTML dashboard (index.html) — live on GitHub Pages |
| AI (Phase 2) | Claude/OpenRouter — not built yet |

## File Structure
```
Career-Copilot/
├── CLAUDE.md                        ✅ This file
├── README.md                        ✅ Setup guide + API reference
├── CAREER_COPILOT_PLAN.md           ✅ Full 13-section architecture doc
├── SETUP.md                         ✅ Supabase + Render setup walkthrough
├── index.html                       ✅ Single-page dashboard (GitHub Pages)
│
├── db/
│   ├── schema.sql                   ✅ Full PostgreSQL schema + RLS
│   ├── seed_companies.sql           ✅ ~50 target companies (original)
│   ├── seed_companies_v2.sql        ✅ ~30 more companies (healthcare, defense, financial, SaaS)
│   └── seed_profile.sql             ✅ Kaleab's candidate profile
│
└── backend/
    ├── .env.example                 ✅ Env var template
    ├── .python-version              ✅ Pins Python 3.11 for Render
    ├── runtime.txt                  ✅ Render Python version fallback
    ├── requirements.txt             ✅ All Python deps
    ├── config.py                    ✅ Pydantic settings loader
    ├── database.py                  ✅ Supabase client singleton
    ├── main.py                      ✅ FastAPI app + CORS + APScheduler (6AM UTC daily)
    ├── ingestion/
    │   ├── normalizer.py            ✅ Role categorization, seniority, salary, dedup
    │   ├── greenhouse.py            ✅ Greenhouse ATS connector (no per-job detail calls)
    │   ├── lever.py                 ✅ Lever ATS connector (description included in list)
    │   └── runner.py                ✅ Orchestrates connectors + auto-scores all users after ingest
    ├── scoring/
    │   └── scorer.py                ✅ 7-dimension weighted scoring engine (ASCII-safe rationale)
    └── routers/
        ├── jobs.py                  ✅ GET /api/jobs, GET /api/jobs/{id}
        ├── applications.py          ✅ Full CRUD — application tracker
        └── ingest.py                ✅ POST /api/ingest, POST /api/ingest/score, GET /api/ingest/status
```

## Scoring System
7 dimensions → composite score → tier:
- role_fit (30%) + growth_fit (20%) + skills_match (20%) + comp_fit (10%) + remote_fit (10%) + company_quality (5%) + realism (5%)

| Tier | Score | Action |
|---|---|---|
| strong_fit | 80–100 | Apply immediately |
| good_fit | 65–79 | Strong candidate, apply |
| stretch | 50–64 | Possible with strong cover letter |
| pass | < 50 | Skip |

## Current Data (as of 2026-04-02)
- **86 companies** in registry (Greenhouse + Lever + HTML placeholders)
- **2,655 jobs** ingested
- **Scoring**: running automatically after each ingest
- **Best matches so far**: Senior Technical Support Engineer @ Cloudflare (70), Senior Endpoint Administrator @ Datadog (66)

## Dashboard Features (live)
- Job board with tier badge filters (Strong / Good / Stretch / Pass)
- **Search bar** — live filter by title, company, location, role category, rationale
- **Age filter** — Last 7 / 14 / 30 days / All time
- **Remote only** toggle
- **Posted date** on each card ("3d ago", "12d ago")
- **Company drill-down** — Companies tab shows job count + "View Jobs" button (filters job board to that company) + Careers page link
- Score breakdown modal (📊 button on each card)
- Application tracker with status pipeline
- Ingest control panel (manual trigger + status)
- Daily auto-ingest at 6AM UTC + auto-score after ingest

## Known Bugs / Limitations
- Greenhouse job descriptions are blank (removed per-job detail fetching to avoid 500+ HTTP calls per company) — fetch on-demand in Phase 2
- No Ashby connector yet — Notion, Vercel, Linear companies show 0 jobs
- skills_match scores low because descriptions are empty (no description = no keyword match)

## What's NOT Built Yet (priority order)
1. **Job description panel** — click to expand full JD fetched on-demand from Greenhouse API
2. **Ashby connector** — adds Notion, Vercel, Linear, etc.
3. **Salary filter** — slider/range on job board
4. **Phase 2: Resume upload + AI tailoring** — PDF upload → Claude match analysis → bullet rewriting → cover letter
5. **Follow-up reminders** — "Applied 7 days ago, follow up?" in Applications tab
6. **Re-score button** — re-run scoring without full re-ingest
7. **Stats/analytics page** — response rate, tier performance over time
8. **Phase 3**: pgvector semantic search, MCP server, CLI layer

## Candidate Profile (Kaleab Tesfaye)
- **Current role**: Desktop Support Specialist III @ Maxim Healthcare
- **Experience**: 4 years IT support
- **User UUID**: 7fe55997-e508-4d10-a7cf-67aa2f81c884
- **Target roles**: Endpoint Administrator, Endpoint Engineer, Systems Administrator, Digital Workplace Specialist, EUC Engineer, MDM Engineer
- **Target categories**: endpoint_management, digital_workplace, systems_admin, mdm_mobility, desktop_engineering
- **Salary**: $65k min, $85k target
- **Remote pref**: preferred
- **Work auth**: US citizen
- **Key skills**: Windows 10/11, Intune/MDM, SCCM, Active Directory, PowerShell, ServiceNow, M365 Admin, device lifecycle

## Pipeline Flow
Daily 6AM UTC → POST /api/ingest → greenhouse.py / lever.py → normalizer.py → upsert jobs → auto-score all users → fit_scores table

## Secrets / Security
- `.env` is gitignored — never commit it
- `SUPABASE_SERVICE_KEY` stays server-side only (backend .env + Render env vars)
- `SUPABASE_ANON_KEY` is safe in index.html (RLS enforced on all tables)
- `ANTHROPIC_API_KEY` — not yet needed, leave blank until Phase 2

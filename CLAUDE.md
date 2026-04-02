# Career Copilot — Claude Context

## What This Is
An AI-powered job search assistant built for Kaleab Tesfaye to land IT growth roles (endpoint management, sysadmin, digital workplace, MDM). Strategic targeting tool — not a spam-apply bot. Monitors target company job boards daily, scores openings against Kaleab's profile, surfaces only roles worth his time.

## Current Status: Phase 0 Backend — COMPLETE

## Tech Stack
| Layer | Tech |
|---|---|
| Backend | Python 3.11 + FastAPI |
| Database | Supabase (PostgreSQL + pgvector + Auth) |
| ATS connectors | Greenhouse + Lever public APIs |
| Frontend | Single-page HTML dashboard (index.html) — live on GitHub Pages |
| AI (Phase 2) | Claude (Anthropic API) — not built yet |

## Live URLs
- **Frontend**: https://kaluzy.github.io/career-copilot/
- **GitHub repo**: https://github.com/Kaluzy/career-copilot

## File Structure
```
Career-Copilot/
├── CLAUDE.md                        ✅ This file
├── README.md                        ✅ Setup guide + API reference
├── CAREER_COPILOT_PLAN.md           ✅ Full 13-section architecture doc
├── index.html                       ✅ Single-page dashboard (GitHub Pages)
│
├── db/
│   ├── schema.sql                   ✅ Full PostgreSQL schema + RLS
│   ├── seed_companies.sql           ✅ ~30 target companies w/ ATS URLs
│   └── seed_profile.sql             ✅ Kaleab's candidate profile seed data
│
└── backend/
    ├── .env.example                 ✅ Env var template (no .env committed)
    ├── requirements.txt             ✅ All Python deps
    ├── config.py                    ✅ Pydantic settings loader
    ├── database.py                  ✅ Supabase client singleton
    ├── main.py                      ✅ FastAPI app + CORS + APScheduler
    ├── ingestion/
    │   ├── normalizer.py            ✅ Role categorization, seniority, salary, dedup
    │   ├── greenhouse.py            ✅ Greenhouse ATS connector (async)
    │   ├── lever.py                 ✅ Lever ATS connector (async)
    │   └── runner.py                ✅ Orchestrates connectors, upserts, scoring
    ├── scoring/
    │   └── scorer.py                ✅ 7-dimension weighted scoring engine
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

## What's NOT Built Yet
- **Phase 0 blocker**: Supabase project setup — migrations not run yet. index.html has placeholder SUPABASE_URL / SUPABASE_ANON_KEY.
- **Phase 1**: React frontend (replaced with single HTML for now — may revisit)
- **Phase 2**: Claude AI rationale, resume tailoring, cover letter generation
- **Phase 3**: pgvector semantic search, MCP server, CLI layer

## Supabase Setup (still pending)
Steps for Kaleab to complete:
1. Create project at supabase.com → name it `career-copilot`
2. SQL Editor → run `db/schema.sql`
3. SQL Editor → run `db/seed_companies.sql`
4. Auth → Users → sign up via the live app → copy UUID
5. SQL Editor → run `db/seed_profile.sql` with UUID substituted
6. Project Settings → API → copy Project URL + anon key
7. Update top 3 lines of `index.html` → commit + push

## Candidate Profile (Kaleab Tesfaye)
- **Current role**: Desktop Support Specialist @ Maxim Healthcare
- **Experience**: 4 years IT support
- **Target roles**: Endpoint Administrator, Endpoint Engineer, Systems Administrator, Digital Workplace Specialist, EUC Engineer, MDM Engineer
- **Target categories**: endpoint_management, digital_workplace, systems_admin, mdm_mobility, desktop_engineering
- **Salary**: $65k min, $85k target
- **Remote pref**: preferred
- **Work auth**: US citizen
- **Key skills**: Windows 10/11, Intune/MDM, SCCM, Active Directory, PowerShell, ServiceNow, M365 Admin, device lifecycle, hardware troubleshooting

## Preferred Companies (partial list)
Cloudflare, Okta, CrowdStrike, Capital One, ServiceNow, Microsoft, Cisco, Palo Alto Networks, SentinelOne, Tanium, Ivanti, Optum, Kaiser Permanente

## Pipeline Flow
Daily 6AM UTC → POST /api/ingest → greenhouse.py / lever.py → normalizer.py → upsert jobs → POST /api/ingest/score → scorer.py → fit_scores table

## Backend Deployment
Not deployed yet. Planned: Render.com (free tier, auto-deploys from GitHub). Backend URL goes in `BACKEND_URL` const in index.html.

## Secrets / Security
- `.env` is gitignored — never commit it
- Only `.env.example` is in the repo
- Supabase anon key is safe for frontend (RLS enforced)
- Service key must stay server-side only (backend .env)

# Career Copilot — Full Project Plan
**Role:** AI-Powered Job Hunter & Application Copilot
**Author:** Senior Product + Solutions Architect + Technical Lead
**Date:** 2026-03-31
**Status:** Planning / Pre-build

---

## TABLE OF CONTENTS

1. Product Definition
2. Functional Requirements
3. Technical Architecture
4. Source Ingestion Strategy
5. Data Model
6. Fit Scoring System
7. Resume Tailoring Engine
8. Application Copilot Workflow
9. MCP and CLI Strategy
10. Roadmap
11. Implementation Sequence
12. Risks and Safeguards
13. Final Recommendation

---

## 1. PRODUCT DEFINITION

### What it is
Career Copilot is a personal, AI-powered job search and application workspace. It ingests job postings from company career sites and trusted boards, scores each job against your real background and career goals, tailors your resume and outreach honestly, and tracks every application through to outcome. It learns from what works.

### Who it is for
IT professionals on a deliberate growth path. Specifically: someone moving beyond desktop support into endpoint management, systems administration, digital workplace, MDM, and IT engineering work — who wants quality over volume and career trajectory over random job hopping.

### User goals
- Find jobs that actually move the career forward — not lateral moves or noise
- Know immediately whether a job is worth applying to
- Tailor resume and messaging truthfully without starting from scratch each time
- Keep all applications organized in one place
- Prepare smarter for interviews based on the actual job requirements
- Learn over time what kind of roles and companies respond positively

### Non-goals
- This is NOT a spam-apply bot
- Does NOT invent skills or fabricate experience
- Does NOT scrape LinkedIn in ways that violate ToS at scale
- Does NOT target unrelated roles (sales, software dev, random startup chaos)
- Does NOT make decisions for you — it advises, you decide

### Success metrics
| Metric | Target |
|--------|--------|
| Jobs ingested per week | 50–150 relevant, filtered |
| Time to score a new job | < 5 seconds |
| Time to tailor resume for a job | < 3 minutes |
| Application-to-response rate | Improve over baseline |
| Callbacks from tailored vs untailored | Track and compare |
| False-positive strong-fit jobs | < 10% |
| Time spent per application (quality) | Down from ~2h to ~30 min |

---

## 2. FUNCTIONAL REQUIREMENTS

### 2.1 Job Search & Ingestion
- Pull jobs from company career sites using direct ATS connectors (Greenhouse, Lever, iCIMS, SmartRecruiters, Workday)
- Fall back to HTML scraping for sites without structured feeds
- Accept manual URL paste for one-off jobs from any source
- Ingest from optional aggregators (Indeed, Adzuna) only for discovery — not as the primary source
- Deduplicate across sources using company + title + date fingerprint
- Normalize all job data to a standard schema regardless of source
- Run on a schedule (daily or configurable)
- Filter before storing: skip obviously irrelevant roles using keyword + role category check

### 2.2 Company Filtering
- Maintain a company quality score (size, stability, structure, growth opportunities)
- Allow user to mark companies as: Preferred / Neutral / Blocked
- Filter out companies user has already been rejected by (configurable)
- Prefer midsize to enterprise employers (500+ employees) unless explicitly flagged otherwise
- Flag companies with known poor culture/growth signals (based on user feedback over time)

### 2.3 Job Fit Scoring
- Score every ingested job across 7 dimensions (see Section 6)
- Produce a composite score: Strong Fit / Good Fit / Stretch / Pass
- Show score breakdown so user understands why a job rated as it did
- Re-score if user updates their profile or resume

### 2.4 Apply / Pass Decisioning
- Surface top jobs in a daily digest view
- Allow user to: Save / Tailor / Apply / Pass / Archive
- Show reasoning for each recommendation
- Warn before passing on a Strong Fit job
- Warn before applying to a Pass-scored job

### 2.5 Resume Tailoring
- Extract requirements, keywords, and must-haves from job posting
- Compare against candidate profile and resume content
- Identify: Strong matches / Partial matches / Gaps
- Rewrite resume bullets to surface relevant real experience
- Generate a tailored professional summary
- Generate a "why this role fits me" reasoning note (for self-review, cover letter source)
- Output: complete tailored resume version linked to that job
- HARD RULE: Never add skills or experience the user doesn't have

### 2.6 Recruiter Message Generation
- Generate a short, direct LinkedIn message or cold email for recruiters
- Generate a cover letter (optional, when required by ATS)
- Generate a polite pass response when declining to apply
- All messages reference real experience, not fabricated content

### 2.7 Application Tracking
- Statuses: Saved → Tailoring → Applied → Screening → Interview → Offer → Rejected → Withdrawn
- Track: application date, response date, next action, notes, contact name
- Reminder system: follow-up prompts at configurable intervals (e.g., 7 days after applying)
- Dashboard view: pipeline by status, open actions, response rate

### 2.8 Feedback Loop
- After each outcome (callback / rejection / offer), record the result
- Tag which resume version, which tailoring approach, which company type, which role level
- Over time: surface patterns ("endpoint engineer roles at midsize companies respond best")
- Feed outcome data back into scoring weights (which job types convert best for this user)

---

## 3. TECHNICAL ARCHITECTURE

### Frontend
**Recommended: React (Vite) + Tailwind CSS**
- SPA hosted on Vercel or Netlify
- Familiar aesthetic to IT Command Center but component-based
- Pages: Dashboard / Job Board / Application Tracker / Resume Editor / Settings
- Mobile-responsive but desktop-first (this is a workspace, not a mobile app)

> Why not single HTML file: The resume editor, job viewer, tailoring panel, and tracker together require state management, routing, and component reuse that a single HTML file cannot handle cleanly past MVP.

### Backend
**Recommended: Python (FastAPI) or Node.js (Express/Hono)**
- REST API consumed by frontend
- Handles: job ingestion, scoring, tailoring requests, tracking CRUD
- Runs scheduled ingestion jobs
- Calls AI APIs (Claude, OpenAI, or similar)
- Python preferred if you want richer text/AI libraries; Node preferred for familiarity with the IT Command Center stack

### Database
**Recommended: Supabase (PostgreSQL)**
- You already use it and understand it
- Handles: companies, jobs, profiles, resumes, applications, scores
- Enable `pgvector` extension for semantic similarity search on job descriptions vs. resume
- Row-level security (same pattern as IT Command Center)
- Free tier covers this project completely at personal scale

### Queue / Scheduler
**Option A (simple): Supabase Edge Functions + pg_cron**
- Schedule daily ingestion job via pg_cron
- No extra infrastructure

**Option B (robust): BullMQ + Redis (Upstash free tier)**
- Job queue for ingestion tasks, scraping, scoring
- Better for retry logic and parallel scraping

Recommendation: Start with Option A. Move to Option B if you add parallel scraping at scale.

### AI / LLM Services
**Primary: Claude API (Anthropic)**
- Resume tailoring, scoring rationale, message generation, interview prep
- Structured output via tool use / JSON mode
- Sonnet model for quality; Haiku for fast batch scoring

**Embeddings: OpenAI text-embedding-3-small or Supabase AI (free)**
- Generate embeddings for job descriptions and resume chunks
- Store in pgvector for semantic similarity matching
- Used for: "find jobs similar to this one I liked"

### Authentication
**Supabase Auth** — same as IT Command Center
- Email/password to start
- Each user has isolated data via RLS

### Storage
**Supabase Storage**
- Store uploaded resume PDF/DOCX files
- Store generated tailored resume versions as PDF or DOCX
- Store cover letters and outreach drafts

### Observability
- **Logging:** Structured logs from API (stdout → log aggregator)
- **Error tracking:** Sentry (free tier)
- **Usage metrics:** Simple Supabase table tracking API calls, scores run, tailoring requests

### Deployment
| Component | Where |
|-----------|-------|
| Frontend | Vercel (free) |
| Backend API | Railway / Render / Fly.io (free tier) |
| Database | Supabase (free) |
| Scheduler | Supabase pg_cron or Upstash QStash |
| File storage | Supabase Storage |
| AI | Claude API (pay per use) |

**Total monthly cost at personal scale: ~$0–$20/month**

---

## 4. SOURCE INGESTION STRATEGY

### Priority 1: Direct ATS Feeds (structured, reliable, no scraping needed)

| ATS | How to ingest | Notes |
|-----|--------------|-------|
| **Greenhouse** | `https://boards-api.greenhouse.io/v1/boards/{company}/jobs` | Free, public JSON API |
| **Lever** | `https://api.lever.co/v0/postings/{company}?mode=json` | Free, public JSON |
| **SmartRecruiters** | `https://api.smartrecruiters.com/v1/companies/{id}/postings` | Public API |
| **Workday** | No public API — HTML parse `myworkdayjobs.com` pages | Needs scraper |
| **iCIMS** | Company-specific portals — HTML fallback | Needs scraper |
| **Ashby** | `https://jobs.ashbyhq.com/{company}/non-applied/job-board-api` | Public JSON |
| **Jobvite** | Company-specific — HTML fallback | Needs scraper |

### How to build the company + ATS registry
```json
{
  "company_id": "microsoft",
  "name": "Microsoft",
  "ats": "workday",
  "ats_url": "https://careers.microsoft.com/...",
  "quality_score": 95,
  "size": "enterprise",
  "remote_friendly": true
}
```
Maintain a curated list of 100–200 target companies. Add new ones manually or via discovery.

### Priority 2: HTML Fallback Scraping (for companies without clean APIs)
- Use **Playwright** (Python) or **Puppeteer** (Node) for JS-rendered pages
- Extract: job title, description, location, posted date, apply URL
- Parse with **BeautifulSoup** (Python) or **Cheerio** (Node)
- Run on a schedule with rate limiting — 1 request per 3–5 seconds per domain
- Handle failures gracefully: log errors, retry once, mark company as "needs manual check"

### Priority 3: Aggregators (discovery only, not primary)
| Source | Use case | Risk |
|--------|---------|------|
| **Indeed API (Adzuna)** | Discover new companies you haven't listed | Low quality, duplicates |
| **Adzuna API** | Free job search API, good for IT roles | Moderate quality |
| **RapidAPI job boards** | Quick access to multiple boards | Variable quality |

Rule: Aggregators find companies you haven't added yet. Once found, add the company to your registry and ingest direct from their ATS next time.

### Job Normalization Schema
Every job, regardless of source, is normalized to:
```json
{
  "source_id": "greenhouse_microsoft_123",
  "source": "greenhouse",
  "company_id": "microsoft",
  "title": "Endpoint Management Specialist",
  "description_raw": "...",
  "description_clean": "...",
  "location": "Remote, USA",
  "remote": true,
  "hybrid": false,
  "salary_min": 85000,
  "salary_max": 115000,
  "posted_at": "2026-03-28",
  "apply_url": "https://...",
  "role_category": "endpoint_management",
  "ingested_at": "2026-03-31T00:00:00Z"
}
```

### Deduplication
- Hash key: `SHA256(company_id + normalized_title + posted_date)`
- If hash exists in DB → skip
- If same company + similar title posted again within 30 days → link as re-post, don't create duplicate

---

## 5. DATA MODEL

### `companies`
```sql
id              uuid PK
name            text
slug            text UNIQUE
ats_type        text        -- greenhouse, lever, workday, html, etc.
ats_url         text
careers_url     text
size            text        -- startup, smb, midsize, enterprise
quality_score   int         -- 0-100 (manually set + AI-assisted)
remote_policy   text        -- remote, hybrid, onsite, unknown
industry        text
notes           text
user_status     text        -- preferred, neutral, blocked, applied_before
created_at      timestamptz
updated_at      timestamptz
```

### `jobs`
```sql
id              uuid PK
company_id      uuid FK → companies
source_id       text UNIQUE     -- dedup key
source          text
title           text
description_raw text
description_clean text
location        text
remote          bool
hybrid          bool
salary_min      int
salary_max      int
role_category   text
seniority       text            -- junior, mid, senior, lead
posted_at       date
apply_url       text
status          text            -- new, scored, saved, applied, archived, expired
embedding       vector(1536)    -- pgvector embedding of description
ingested_at     timestamptz
expires_at      timestamptz
```

### `candidate_profile`
```sql
id              uuid PK
user_id         uuid FK → auth.users
full_name       text
current_title   text
current_company text
years_experience int
skills          jsonb       -- [{skill, level, years}]
target_roles    text[]
target_titles   text[]
avoid_roles     text[]
salary_min      int
salary_target   int
locations       text[]
remote_pref     text        -- required, preferred, open
work_auth       text
career_summary  text
updated_at      timestamptz
```

### `resume_assets`
```sql
id              uuid PK
user_id         uuid FK
version_name    text        -- "Master", "Endpoint Focus v2"
file_url        text        -- Supabase Storage
content_parsed  jsonb       -- structured: summary, experience[], skills[], education[]
is_master       bool
created_at      timestamptz
```

### `tailored_resumes`
```sql
id              uuid PK
job_id          uuid FK → jobs
user_id         uuid FK
base_resume_id  uuid FK → resume_assets
tailored_content jsonb      -- modified bullets, summary, keywords added
match_analysis   jsonb      -- strong_matches[], partial_matches[], gaps[]
cover_letter    text
file_url        text        -- generated PDF
created_at      timestamptz
```

### `fit_scores`
```sql
id              uuid PK
job_id          uuid FK
user_id         uuid FK
role_fit        int         -- 0-100
growth_fit      int
comp_fit        int
remote_fit      int
company_quality int
realism         int         -- how realistic is it to get this role
effort_value    int         -- worth the tailoring effort?
composite       int         -- weighted total
tier            text        -- strong_fit, good_fit, stretch, pass
rationale       text        -- AI-generated reasoning
scored_at       timestamptz
```

### `applications`
```sql
id              uuid PK
job_id          uuid FK
user_id         uuid FK
tailored_resume_id uuid FK
status          text        -- saved, tailoring, applied, screening, interview, offer, rejected, withdrawn
applied_at      timestamptz
response_at     timestamptz
next_action     text
next_action_at  timestamptz
contact_name    text
contact_email   text
notes           text
source_channel  text        -- direct, linkedin, referral, recruiter
updated_at      timestamptz
```

### `outcomes`
```sql
id              uuid PK
application_id  uuid FK
result          text        -- callback, phone_screen, technical, onsite, offer, rejected_after_apply, ghosted
result_at       timestamptz
rejection_reason text
salary_offered  int
notes           text
```

### `company_quality_scores`
```sql
id              uuid PK
company_id      uuid FK
score           int         -- 0-100
factors         jsonb       -- {size, stability, glassdoor, growth_path, remote_policy}
last_reviewed   date
```

---

## 6. FIT SCORING SYSTEM

### The 7 Dimensions (weighted)

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| **Role Fit** | 30% | How well the job title and responsibilities match your target roles |
| **Growth Fit** | 20% | Does this role move you toward endpoint/sysadmin/engineering? |
| **Skills Match** | 20% | What % of required skills/tools you actually have |
| **Comp Fit** | 10% | Salary range vs. your target |
| **Remote/Location Fit** | 10% | Remote/hybrid availability |
| **Company Quality** | 5% | Size, stability, structure, growth path |
| **Realism** | 5% | How likely are you to get an interview (seniority, req match) |

### Composite Score → Tier

| Composite | Tier | Action |
|-----------|------|--------|
| 80–100 | **Strong Fit** | Prioritize — tailor and apply this week |
| 65–79 | **Good Fit** | Apply when you have time — tailor thoughtfully |
| 50–64 | **Stretch** | Consider if company is exceptional — flag gaps clearly |
| < 50 | **Pass** | Not worth your time — archive automatically |

### Scoring Examples

**Example 1 — Strong Fit (score: 88)**
- Job: Endpoint Management Specialist, midsize healthcare company, hybrid
- Role: Matches target title exactly
- Growth: Direct path into endpoint engineering
- Skills: 85% match (SCCM, Intune, Windows imaging, PowerShell)
- Comp: $90k–$110k — hits target
- Remote: Hybrid — preferred
- Company: 2,000 employees, stable, IT structure
- Realism: Mid-level req — realistic match
→ **Priority apply. Tailor now.**

**Example 2 — Good Fit (score: 71)**
- Job: Systems Administrator, regional law firm, onsite
- Role: Sysadmin is a target title
- Growth: Good step up
- Skills: 65% match (AD, Group Policy — know it; Linux — limited)
- Comp: $75k–$85k — slightly below target
- Remote: Onsite only — not preferred but acceptable
- Company: 300 employees, stable
- Realism: Good match
→ **Apply when you can. Note Linux gap.**

**Example 3 — Stretch but Realistic (score: 56)**
- Job: Infrastructure Engineer, enterprise bank, hybrid
- Role: Beyond current level — stretch title
- Growth: High value if you get it
- Skills: 45% match (strong on endpoint, weak on networking/cloud infra)
- Comp: $100k–$120k — above target
- Remote: Hybrid — good
- Company: Enterprise, very structured
- Realism: Lower — likely needs more infra experience
→ **Save it. Apply only with a strong referral or if you have a network contact.**

**Example 4 — Pass (score: 32)**
- Job: Help Desk Technician I, small startup, onsite
- Role: Step backward
- Growth: None — same or lower level
- Skills: Overqualified
- Comp: $45k–$55k — below target
- Remote: Onsite only
- Company: 15-person startup, no structure
→ **Auto-archive. Do not apply.**

---

## 7. RESUME TAILORING ENGINE

### Step 1 — Parse the job posting
Extract and structure:
- Required skills (hard requirements)
- Preferred skills (nice to have)
- Tools and platforms mentioned (Intune, SCCM, Jamf, Ansible, etc.)
- Role responsibilities
- Keywords likely used by ATS (exact phrases from posting)
- Seniority signals
- Keywords to avoid (if not relevant to you)

### Step 2 — Compare against your profile + resume
For each requirement:
- **Strong match:** You have it, it's in your resume, bullet is strong → keep or strengthen
- **Partial match:** You have related experience but not exact → reframe existing bullet to show relevance
- **Gap:** You don't have it → note it, never fabricate, sometimes address in cover letter

Produce a match analysis:
```json
{
  "strong_matches": ["Windows 10/11 imaging", "Intune MDM", "SCCM deployment"],
  "partial_matches": ["PowerShell scripting (have it, not prominently featured)", "Jamf (limited, mention as exposure)"],
  "gaps": ["Linux administration", "Azure AD Conditional Access"],
  "ats_keywords_to_include": ["endpoint management", "device lifecycle", "remote remediation"]
}
```

### Step 3 — Rewrite resume bullets (truthfully)
**Original bullet:**
> "Provided desktop support for 500+ users including hardware and software troubleshooting"

**Tailored bullet (for endpoint management role):**
> "Supported 500+ endpoint users across Windows 10/11 devices, resolving hardware, OS, and application issues through remote tools and on-site remediation"

Rules:
- Only add detail you actually did
- Surface relevant tools if you used them (even if not your main task)
- Use the posting's language/keywords where they honestly apply
- Quantify where possible

### Step 4 — Generate tailored professional summary
Takes your master summary + job requirements → writes a 3-sentence summary specific to this role.

Example output for an Endpoint Specialist role:
> "IT support professional with 4+ years of experience in endpoint management, device deployment, and remote remediation across enterprise Windows environments. Experienced with Intune, SCCM, and device lifecycle management in healthcare and enterprise settings. Seeking to grow into a dedicated endpoint operations role with a focus on automation and scalable device management."

### Step 5 — "Why this role fits me" note
A private note for your own review (not sent to employer):
> "Strong match: my Intune and SCCM work aligns directly. Partial: I have PowerShell but should lead with it more. Gap: they want Jamf — I have no Mac MDM experience. Company is in healthcare — I have healthcare endpoint context from Maxim. This is worth applying to."

---

## 8. APPLICATION COPILOT WORKFLOW

### Full workflow for one application

```
1. DISCOVER
   Job ingested automatically (or pasted manually)
   → Scored immediately
   → Appears in job board with tier badge

2. REVIEW
   User opens job card
   → Sees: score breakdown, match analysis, company info
   → Decision: Save / Pass / Start Tailoring

3. TAILOR
   User clicks "Tailor Resume"
   → System shows: strong matches, partials, gaps
   → AI rewrites relevant bullets
   → User reviews and edits (always in control)
   → User approves tailored version
   → PDF generated and linked to this job

4. OUTREACH (optional)
   If company allows direct contact or LinkedIn recruiter found:
   → Generate short recruiter message (3–4 sentences, honest, direct)
   → User reviews and sends manually

5. APPLY
   User applies on company site
   → Mark as Applied in tracker
   → Application date recorded
   → Follow-up reminder set (default: 7 days)

6. TRACK
   Status updated as events happen:
   Screening call booked → update status
   Interview scheduled → system generates prep notes (from job requirements + your background)
   Outcome recorded → callback / rejection / offer

7. INTERVIEW PREP
   User opens prep panel:
   → Likely questions based on job requirements
   → Your relevant experience mapped to each question area
   → Technical topics to review based on gap analysis
   → STAR story prompts for behavioral questions

8. OUTCOME & LEARN
   After outcome is recorded:
   → System notes: what tier, what company type, what tailoring approach
   → Over time: patterns surface ("your callback rate on Endpoint Specialist roles is 40% vs 12% on Sysadmin stretch roles")
```

### Follow-up decision logic
- 7 days after apply → remind to follow up (if no response)
- 14 days → suggest a polite follow-up message or move to "likely ghosted"
- 30 days with no response → auto-archive with outcome: ghosted

---

## 9. MCP AND CLI STRATEGY

### Why MCP and CLI matter for this project
- MCP: lets you use Career Copilot as a tool inside Claude or any AI environment. Ask Claude "find me endpoint jobs posted this week" and it calls your own backend.
- CLI: lets you run jobs, check status, trigger ingestion from terminal without opening a browser.

### CLI (`copilot` command)

```bash
# Ingest new jobs from all configured sources
copilot ingest

# Ingest from a specific company
copilot ingest --company microsoft

# Score all unscored jobs
copilot score

# Show today's top jobs
copilot jobs --tier strong_fit
copilot jobs --tier good_fit --limit 10

# Add a job manually by URL
copilot add-job https://boards.greenhouse.io/company/jobs/123

# Save a job for tailoring
copilot save <job_id>

# Tailor resume for a job
copilot tailor <job_id>

# Mark a job as applied
copilot apply <job_id>

# Show application pipeline
copilot pipeline

# Show stats / feedback summary
copilot stats
```

### MCP Server Tools

The MCP server exposes your backend as tools callable by Claude or any MCP client.

| Tool | Input | Output |
|------|-------|--------|
| `find_jobs` | role_category, tier, limit | List of matching jobs with scores |
| `fetch_job` | job_id | Full job details, description, company info |
| `score_job_fit` | job_id (or raw description) | Fit score + tier + rationale |
| `tailor_resume` | job_id | Match analysis + tailored bullets + summary |
| `draft_recruiter_note` | job_id | Short outreach message |
| `draft_cover_letter` | job_id | Full cover letter |
| `save_job` | job_id | Saves job to tracker |
| `mark_applied` | job_id, date | Updates application status |
| `get_pipeline` | — | Current application statuses |
| `get_stats` | — | Callback rates, tier performance |
| `add_company` | name, ats_type, ats_url | Adds company to ingestion registry |

### MCP server setup (simple)
Built with the **Claude Agent SDK** or **MCP Python SDK**:
```python
@mcp.tool()
def find_jobs(role_category: str, tier: str = "strong_fit", limit: int = 10):
    """Find scored jobs matching the given category and tier"""
    return db.query("""
        SELECT j.*, f.tier, f.composite, f.rationale
        FROM jobs j JOIN fit_scores f ON j.id = f.job_id
        WHERE j.role_category = %s AND f.tier = %s
        ORDER BY f.composite DESC LIMIT %s
    """, [role_category, tier, limit])
```

---

## 10. ROADMAP

### MVP — "Find and score" (4–6 weeks to build)
**Goal:** Working job board with ingestion, scoring, and basic tracking. No AI tailoring yet.

- [ ] Supabase schema (companies, jobs, candidate_profile, fit_scores, applications)
- [ ] Company registry with 30–50 target companies
- [ ] Greenhouse + Lever connectors (structured, reliable, quick to build)
- [ ] Job normalization and deduplication
- [ ] Basic rule-based fit scoring (keyword match + role category match)
- [ ] Simple React frontend: job board view, score badges, save/pass buttons
- [ ] Application tracker: status column board (like the IT queue board)
- [ ] Daily ingestion scheduler (Supabase pg_cron)
- [ ] Deploy: Vercel (frontend) + Railway (backend) + Supabase (db)

**Outcome:** You wake up every morning, open the dashboard, and see new scored jobs from companies you care about — without searching manually.

---

### Phase 2 — "Tailor and apply" (4–6 weeks after MVP)
**Goal:** AI-powered resume tailoring and outreach generation.

- [ ] Resume upload + parsing (PDF → structured JSON)
- [ ] AI match analysis per job (Claude API)
- [ ] AI-powered resume bullet rewriting
- [ ] Tailored resume PDF generation
- [ ] Recruiter message + cover letter generation
- [ ] Interview prep panel (question suggestions based on job requirements)
- [ ] AI-powered scoring rationale (replace rule-based scoring with LLM scoring)
- [ ] Supabase Storage for resume versions
- [ ] Feedback tagging on applications (what tier, what role type, what approach)

**Outcome:** You go from "here's a job" to "here's your tailored resume, outreach message, and prep notes" in under 5 minutes.

---

### Phase 3 — "Learn and improve" (4–8 weeks after Phase 2)
**Goal:** Feedback loop, semantic search, pattern recognition.

- [ ] Outcome recording (callback / rejection / offer)
- [ ] Feedback loop: outcomes → scoring weight adjustments
- [ ] pgvector embeddings on job descriptions + resume
- [ ] Semantic job similarity: "find jobs similar to this one I got a callback on"
- [ ] CLI (`copilot` command) for terminal-first workflows
- [ ] MCP server exposing all tools to Claude
- [ ] Company quality scoring (automated + manual hybrid)
- [ ] Notification / digest emails (weekly top jobs summary)
- [ ] HTML fallback scraper for Workday, iCIMS, Jobvite

**Outcome:** The system gets smarter over time. It knows which role types convert for you and prioritizes them. You can ask Claude "what should I apply to this week?" and get a real answer.

---

### Stretch Goals
- Resume version A/B testing (track which version gets more responses)
- Salary intelligence (aggregate comp data by role + location)
- Referral network tracker (who do you know at which companies)
- Auto-apply to fully structured ATS jobs with your approval
- Browser extension: "add this job to Career Copilot" from any page
- Mobile app (React Native or PWA)
- Integration with your IT Command Center (closed tickets → new skills to add to profile)

---

## 11. IMPLEMENTATION SEQUENCE

### Phase 0: Foundation (Week 1)
1. Create Supabase project, run schema migrations
2. Create candidate profile with your real background
3. Add 30–50 target companies to company registry with ATS info
4. Test one Greenhouse connector manually (pull jobs, normalize, store)
5. Set up project repo structure

### Phase 1: Ingestion + Scoring (Weeks 2–4)
6. Build Greenhouse and Lever connectors
7. Build normalization + deduplication pipeline
8. Build rule-based fit scorer (keyword + role category matching)
9. Build FastAPI/Express backend with ingestion endpoints
10. Set up pg_cron for daily ingestion
11. Test: ingest 50 real jobs, review scores manually for accuracy

### Phase 2: Frontend (Weeks 3–5, parallel with backend)
12. React app scaffold with Vite + Tailwind
13. Job board page (list view, score badges, filter by tier)
14. Job detail modal (description, score breakdown, company info)
15. Application tracker (kanban: saved → applied → interview → outcome)
16. Candidate profile page
17. Deploy to Vercel

### Phase 3: AI Tailoring (Weeks 6–9)
18. Resume upload + PDF parsing
19. Claude API integration for match analysis
20. Bullet rewriting UI (side-by-side: original vs tailored)
21. Recruiter message generation
22. Cover letter generation
23. Tailored resume export (PDF via html-to-pdf or similar)

### Phase 4: CLI + MCP (Weeks 10–12)
24. CLI with `ingest`, `jobs`, `save`, `tailor`, `apply` commands
25. MCP server with core tools
26. Test MCP tools from within Claude

### Phase 5: Feedback Loop (Weeks 13–16)
27. Outcome recording UI
28. Scoring weight adjustments based on outcomes
29. pgvector embeddings + semantic search
30. Stats / analytics page

---

## 12. RISKS AND SAFEGUARDS

### Legal / Compliance
| Risk | Mitigation |
|------|-----------|
| Scraping ToS violations | Use public ATS APIs first. Only scrape public career pages, not behind-login content. Rate limit all requests. |
| GDPR / data privacy | This is personal data you own. Don't share it with third parties unnecessarily. |
| AI-generated content in applications | Always review before sending. Never auto-submit. |

### Resume Honesty
| Risk | Mitigation |
|------|-----------|
| AI adds fake skills | Hard rule: tailoring only reframes existing experience, never adds new skills. Gaps are surfaced, not filled. |
| Overstated bullets | Every generated bullet is shown to you for review before use. You approve every change. |
| Cover letters that overclaim | Prompt includes explicit instruction: "Only reference experience in the candidate profile. If a requirement is not met, acknowledge the gap rather than fabricate." |

### Over-automation
| Risk | Mitigation |
|------|-----------|
| Applying to too many jobs | System is advisory, not auto-apply. You approve every application. |
| Ignoring pass-rated jobs | System flags but does not block — you can override a Pass if you have context the system doesn't |
| Trusting scores blindly | Score rationale always shown. You decide. |

### Scraping Fragility
| Risk | Mitigation |
|------|-----------|
| Sites change their HTML | Normalize all scraping into adapters. When adapter breaks, flag company as "manual check needed" — don't crash the pipeline. |
| IP blocking | Rate limit. Use rotating headers. Don't hammer any single domain. |
| Jobs expire | Track `expires_at`, auto-archive jobs older than 30 days with no re-post. |

### Bad-Fit Application Risk
| Risk | Mitigation |
|------|-----------|
| Applying to stretch roles too aggressively | Stretch tier requires explicit user confirmation. System warns: "This role has skill gaps you haven't addressed." |
| Applying to low-quality companies | Company quality score gates what gets surfaced. Blocked companies never appear. |

### Privacy
| Risk | Mitigation |
|------|-----------|
| Resume data sent to AI APIs | Claude API does not train on API-submitted data. Acceptable for personal use. |
| Job data stored in Supabase | Your own Supabase project, your own row-level security. No third party has access. |

---

## 13. FINAL RECOMMENDATION

### Recommended Architecture

```
Frontend:     React (Vite) + Tailwind CSS → Vercel
Backend:      FastAPI (Python) → Railway
Database:     Supabase (PostgreSQL + pgvector + Storage + Auth)
Scheduler:    Supabase pg_cron (simple) → upgrade to BullMQ if needed
AI:           Claude API (Anthropic) for tailoring + scoring rationale
Embeddings:   OpenAI text-embedding-3-small or Supabase AI
CLI:          Python Click or Typer
MCP:          Python MCP SDK
```

**Why this stack:**
- You already understand Supabase — zero learning curve on DB/auth/storage
- FastAPI is clean, fast, well-documented, and excellent for AI-heavy backends
- React with Vite + Tailwind gives you the same clean look as your IT Command Center
- Claude is the right AI for nuanced, honest resume tailoring — it follows instructions reliably
- Railway + Vercel are both free tier at personal scale

---

### Recommended MVP (build this first)

**4 weeks. One goal: Wake up every morning and see new scored jobs you care about.**

Scope:
1. Supabase schema live
2. 40 target companies in registry
3. Greenhouse + Lever connectors working
4. Daily ingestion via pg_cron
5. Keyword-based fit scoring (no AI yet — rule-based is fine for MVP)
6. Simple React job board: list view, tier badges, Save / Pass buttons
7. Basic application tracker (status column)
8. Deployed and accessible from browser

**What this proves:** The ingestion and scoring engine works. You're getting real value before the AI tailoring even exists.

Then in Phase 2, layer in Claude for tailoring and the whole system becomes your application workspace.

---

### Final note on discipline

The biggest risk to a project like this is not technical — it's that you start applying to jobs you shouldn't just because the system found them. The scoring system is only as good as the weights, and the tailoring only as good as your honesty about what you actually know.

The safeguard is this: **always review, always decide, never auto-apply.**

This system is a copilot — not an autopilot. It does the research, the comparison, the drafting. You decide what to send and where to go. That discipline is what makes it a career tool and not a spam machine.

---

*Document ends.*
*Next step: Begin Phase 0 — Supabase schema + company registry.*

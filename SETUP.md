# Career Copilot — Setup Guide

Everything you need to do to get this running. Do these steps in order.

---

## Step 1 — Create the Supabase project

1. Go to [supabase.com](https://supabase.com) → sign in → **New project**
2. Name it `career-copilot`
3. Choose a strong database password — **save it somewhere safe**
4. Region: `US East` (or closest to you)
5. Click **Create new project** — wait ~2 minutes for it to provision

---

## Step 2 — Run the database schema

1. In your Supabase project, click **SQL Editor** in the left sidebar
2. Click **New query**
3. Open `db/schema.sql` from this project folder
4. Copy the entire contents → paste into the SQL editor
5. Click **Run** (or Ctrl+Enter)
6. You should see: `Success. No rows returned`

> This creates all 9 tables, indexes, and row-level security policies.

---

## Step 3 — Seed the company registry

1. In SQL Editor → **New query**
2. Open `db/seed_companies.sql` from this project folder
3. Copy entire contents → paste → **Run**
4. You should see: `Success. X rows affected`

> This loads ~30 target companies with their ATS connectors pre-configured.

---

## Step 4 — Create your user account

1. In Supabase → **Authentication** (left sidebar) → **Users** tab
2. Click **Add user** → **Create new user**
3. Enter your email and a password
4. Click **Create user**
5. **Copy your User UID** — the UUID shown next to your email. You'll need it in Step 5.

---

## Step 5 — Seed your candidate profile

1. Open `db/seed_profile.sql` in a text editor
2. Find the line: `'YOUR-USER-UUID-HERE'`
3. Replace it with the UUID you copied in Step 4
4. In Supabase SQL Editor → **New query**
5. Paste the modified SQL → **Run**

---

## Step 6 — Get your API keys

1. In Supabase → **Project Settings** (gear icon, bottom left) → **API**
2. Copy two values:
   - **Project URL** — looks like `https://xxxxxxxxxxxx.supabase.co`
   - **anon public** key — long string under "Project API keys"

---

## Step 7 — Update index.html

Open `index.html` in this project folder. Find lines 70–72 at the top of the `<script>` block:

```js
const SUPABASE_URL     = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
const BACKEND_URL      = 'YOUR_BACKEND_URL';
```

Replace with your actual values:

```js
const SUPABASE_URL     = 'https://xxxxxxxxxxxx.supabase.co';
const SUPABASE_ANON_KEY = 'eyJh...your anon key...';
const BACKEND_URL      = '';   // leave empty for now — fill in after backend deploy
```

Save the file.

---

## Step 8 — Push index.html to GitHub Pages

```bash
git add index.html
git commit -m "Connect Supabase project"
git push
```

Wait ~60 seconds → visit `https://kaluzy.github.io/career-copilot/`

The dashboard should load and show the login form. Sign in with the credentials you created in Step 4.

---

## Step 9 — Set up the backend .env

In the `backend/` folder, create a `.env` file (copy from `.env.example`):

```
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_SERVICE_KEY=<your service_role key from Supabase → API → service_role>
ANTHROPIC_API_KEY=<your Claude API key — needed for Phase 2>
```

> **Never commit `.env` — it's already in .gitignore.**
> The service key is different from the anon key. It has full DB access and must stay server-side only.

---

## Step 10 — Test the backend locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Then in a browser or terminal:

```bash
# Trigger ingestion manually
curl -X POST http://localhost:8000/api/ingest

# Check status
curl http://localhost:8000/api/ingest/status

# List scored jobs
curl http://localhost:8000/api/jobs
```

If ingestion works, you'll see jobs appear in the Supabase `jobs` table and on the dashboard.

---

## Step 11 — Deploy the backend to Render

1. Go to [render.com](https://render.com) → sign in with GitHub
2. **New** → **Web Service** → connect your `career-copilot` repo
3. Settings:
   - **Root directory:** `backend`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Under **Environment** → add all vars from your `.env`:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `ANTHROPIC_API_KEY`
5. Click **Create Web Service**
6. Once deployed, copy the Render URL (looks like `https://career-copilot-xxxx.onrender.com`)

---

## Step 12 — Wire backend URL into index.html

Update line 72 in `index.html`:

```js
const BACKEND_URL = 'https://career-copilot-xxxx.onrender.com';
```

Commit and push. Dashboard's **Ingest Now** button will now trigger real ingestion.

---

## You're live

| Component | Status after setup |
|---|---|
| Database | Supabase — schema + seed data loaded |
| Auth | Your account created, profile seeded |
| Dashboard | GitHub Pages — `kaluzy.github.io/career-copilot` |
| Backend | Render — auto-ingesting daily at 6AM UTC |

---

## What to do next (Phase 2)

Once ingestion is running and you're seeing real jobs scored in the dashboard:

1. Upload your resume PDF → parsing + Claude AI tailoring (Phase 2 build)
2. Add more companies to `seed_companies.sql` → re-run the seed
3. Adjust scoring weights in `backend/scoring/scorer.py` if fit tiers feel off

See [CAREER_COPILOT_PLAN.md](CAREER_COPILOT_PLAN.md) for the full Phase 2 roadmap.

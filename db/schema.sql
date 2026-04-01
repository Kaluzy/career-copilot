-- ============================================================
-- Career Copilot — Database Schema
-- Run this in your Supabase SQL editor
-- ============================================================

-- Enable pgvector for semantic search (Phase 3)
CREATE EXTENSION IF NOT EXISTS vector;

-- ── Companies ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS companies (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name          text NOT NULL,
  slug          text UNIQUE NOT NULL,
  ats_type      text,             -- greenhouse | lever | workday | smartrecruiters | ashby | html
  ats_slug      text,             -- the company's slug in their ATS (e.g. "okta" in greenhouse)
  ats_url       text,             -- full ingestion URL
  careers_url   text,             -- public careers page
  size          text,             -- startup | smb | midsize | enterprise
  quality_score int DEFAULT 70 CHECK (quality_score BETWEEN 0 AND 100),
  remote_policy text DEFAULT 'unknown',  -- remote | hybrid | onsite | unknown
  industry      text,
  hq_location   text,
  notes         text,
  user_status   text DEFAULT 'neutral', -- preferred | neutral | blocked
  active        bool DEFAULT true,
  created_at    timestamptz DEFAULT now(),
  updated_at    timestamptz DEFAULT now()
);

-- ── Jobs ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jobs (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id       uuid REFERENCES companies(id) ON DELETE CASCADE,
  source_id        text UNIQUE,     -- dedup: ats_type + slug + job_id
  source           text,
  title            text NOT NULL,
  description_raw  text,
  description_clean text,
  location         text,
  remote           bool DEFAULT false,
  hybrid           bool DEFAULT false,
  salary_min       int,
  salary_max       int,
  role_category    text,            -- endpoint_management | sysadmin | mdm | digital_workplace | etc.
  seniority        text,            -- junior | mid | senior | lead | unknown
  posted_at        date,
  apply_url        text,
  status           text DEFAULT 'new',  -- new | scored | saved | applied | archived | expired
  embedding        vector(1536),    -- for Phase 3 semantic search
  ingested_at      timestamptz DEFAULT now(),
  expires_at       timestamptz GENERATED ALWAYS AS (ingested_at + INTERVAL '45 days') STORED
);

-- ── Candidate Profile ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS candidate_profile (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id           uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name         text,
  current_title     text,
  current_company   text,
  years_experience  int,
  skills            jsonb DEFAULT '[]',  -- [{skill, level, years_exp}]
  tools             jsonb DEFAULT '[]',  -- [{tool, proficiency}]
  target_roles      text[],
  target_titles     text[],
  avoid_roles       text[],
  salary_min        int,
  salary_target     int,
  locations         text[],
  remote_pref       text DEFAULT 'preferred',  -- required | preferred | open
  work_auth         text DEFAULT 'us_citizen',
  career_summary    text,
  linkedin_url      text,
  updated_at        timestamptz DEFAULT now()
);

-- ── Resume Assets ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS resume_assets (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  version_name    text DEFAULT 'Master',
  file_url        text,
  content_parsed  jsonb,  -- {summary, experience:[{title, company, dates, bullets:[]}], skills:[], education:[]}
  is_master       bool DEFAULT false,
  created_at      timestamptz DEFAULT now()
);

-- ── Fit Scores ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fit_scores (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id          uuid REFERENCES jobs(id) ON DELETE CASCADE,
  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  role_fit        int DEFAULT 0 CHECK (role_fit BETWEEN 0 AND 100),
  growth_fit      int DEFAULT 0 CHECK (growth_fit BETWEEN 0 AND 100),
  skills_match    int DEFAULT 0 CHECK (skills_match BETWEEN 0 AND 100),
  comp_fit        int DEFAULT 0 CHECK (comp_fit BETWEEN 0 AND 100),
  remote_fit      int DEFAULT 0 CHECK (remote_fit BETWEEN 0 AND 100),
  company_quality int DEFAULT 0 CHECK (company_quality BETWEEN 0 AND 100),
  realism         int DEFAULT 0 CHECK (realism BETWEEN 0 AND 100),
  composite       int DEFAULT 0 CHECK (composite BETWEEN 0 AND 100),
  tier            text DEFAULT 'pass',  -- strong_fit | good_fit | stretch | pass
  rationale       text,
  scored_at       timestamptz DEFAULT now(),
  UNIQUE(job_id, user_id)
);

-- ── Tailored Resumes ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS tailored_resumes (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id           uuid REFERENCES jobs(id) ON DELETE CASCADE,
  user_id          uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  base_resume_id   uuid REFERENCES resume_assets(id),
  tailored_content jsonb,   -- modified bullets and summary
  match_analysis   jsonb,   -- {strong_matches, partial_matches, gaps, ats_keywords}
  cover_letter     text,
  recruiter_note   text,
  interview_prep   text,
  file_url         text,
  created_at       timestamptz DEFAULT now()
);

-- ── Applications ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS applications (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id              uuid REFERENCES jobs(id) ON DELETE CASCADE,
  user_id             uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  tailored_resume_id  uuid REFERENCES tailored_resumes(id),
  status              text DEFAULT 'saved',
  -- saved | tailoring | applied | screening | interview | offer | rejected | withdrawn
  applied_at          timestamptz,
  response_at         timestamptz,
  next_action         text,
  next_action_at      timestamptz,
  contact_name        text,
  contact_email       text,
  notes               text,
  source_channel      text,  -- direct | linkedin | referral | recruiter
  updated_at          timestamptz DEFAULT now()
);

-- ── Outcomes ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS outcomes (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id    uuid REFERENCES applications(id) ON DELETE CASCADE,
  result            text,
  -- callback | phone_screen | technical | onsite | offer | rejected_after_apply | ghosted | withdrawn
  result_at         timestamptz DEFAULT now(),
  rejection_reason  text,
  salary_offered    int,
  notes             text
);

-- ── System settings (internal key-value store) ───────────
CREATE TABLE IF NOT EXISTS system_settings (
  key        text PRIMARY KEY,
  value      jsonb,
  updated_at timestamptz DEFAULT now()
);

-- ── Indexes ───────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_role_category ON jobs(role_category);
CREATE INDEX IF NOT EXISTS idx_jobs_ingested ON jobs(ingested_at DESC);
CREATE INDEX IF NOT EXISTS idx_fit_scores_user ON fit_scores(user_id);
CREATE INDEX IF NOT EXISTS idx_fit_scores_tier ON fit_scores(tier);
CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);

-- ── Row Level Security ────────────────────────────────────
ALTER TABLE companies        ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs             ENABLE ROW LEVEL SECURITY;
ALTER TABLE candidate_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE resume_assets    ENABLE ROW LEVEL SECURITY;
ALTER TABLE fit_scores       ENABLE ROW LEVEL SECURITY;
ALTER TABLE tailored_resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications     ENABLE ROW LEVEL SECURITY;
ALTER TABLE outcomes         ENABLE ROW LEVEL SECURITY;

-- Companies + jobs: any authenticated user can read (shared job pool)
-- Backend service role bypasses RLS for ingestion
CREATE POLICY "read_companies" ON companies FOR SELECT TO authenticated USING (true);
CREATE POLICY "read_jobs"      ON jobs      FOR SELECT TO authenticated USING (true);

-- Personal data: owner only
CREATE POLICY "owner_profile"     ON candidate_profile  FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "owner_resumes"     ON resume_assets      FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "owner_scores"      ON fit_scores         FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "owner_tailored"    ON tailored_resumes   FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "owner_applications" ON applications      FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "owner_outcomes"    ON outcomes           FOR ALL USING (
  EXISTS (SELECT 1 FROM applications a WHERE a.id = application_id AND a.user_id = auth.uid())
);

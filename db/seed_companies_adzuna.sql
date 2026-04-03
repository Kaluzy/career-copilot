-- Adzuna sentinel row — one fake "company" that triggers the Adzuna search connector.
-- The connector ignores company fields and runs keyword searches instead.
-- Run in Supabase SQL editor.

INSERT INTO companies (name, slug, ats_type, ats_slug, careers_url, quality_score, active)
VALUES (
  'Adzuna Search',
  'adzuna',
  'adzuna',
  'adzuna',
  'https://www.adzuna.com',
  75,
  true
)
ON CONFLICT (slug) DO UPDATE SET
  ats_type    = EXCLUDED.ats_type,
  ats_slug    = EXCLUDED.ats_slug,
  active      = EXCLUDED.active;

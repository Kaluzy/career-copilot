-- SmartRecruiters ATS companies — IT/security/SaaS companies known to use SmartRecruiters
-- Run in Supabase SQL editor

INSERT INTO companies (name, slug, ats_type, ats_slug, careers_url, quality_score, active)
VALUES
  ('TEKsystems',         'teksystems',         'smartrecruiters', 'TEKsystems',         'https://jobs.smartrecruiters.com/TEKsystems',         80, true),
  ('Insight Global',     'insight-global',     'smartrecruiters', 'InsightGlobal',      'https://jobs.smartrecruiters.com/InsightGlobal',      78, true),
  ('Kforce',             'kforce',             'smartrecruiters', 'Kforce',             'https://jobs.smartrecruiters.com/Kforce',             76, true),
  ('Modis',              'modis',              'smartrecruiters', 'Modis',              'https://jobs.smartrecruiters.com/Modis',              74, true),
  ('Leidos',             'leidos',             'smartrecruiters', 'Leidos',             'https://jobs.smartrecruiters.com/Leidos',             82, true),
  ('SAIC',               'saic',               'smartrecruiters', 'SAIC',               'https://jobs.smartrecruiters.com/SAIC',               81, true),
  ('Unisys',             'unisys',             'smartrecruiters', 'Unisys',             'https://jobs.smartrecruiters.com/Unisys',             75, true),
  ('Conduent',           'conduent',           'smartrecruiters', 'Conduent',           'https://jobs.smartrecruiters.com/Conduent',           72, true),
  ('DXC Technology',     'dxc-technology',     'smartrecruiters', 'DXCTechnology',      'https://jobs.smartrecruiters.com/DXCTechnology',      76, true),
  ('Cognizant',          'cognizant',          'smartrecruiters', 'Cognizant',          'https://jobs.smartrecruiters.com/Cognizant',          78, true)
ON CONFLICT (slug) DO UPDATE SET
  ats_type    = EXCLUDED.ats_type,
  ats_slug    = EXCLUDED.ats_slug,
  careers_url = EXCLUDED.careers_url,
  quality_score = EXCLUDED.quality_score,
  active      = EXCLUDED.active;

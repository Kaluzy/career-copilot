-- Ashby ATS companies — IT/SaaS/Security companies known to use Ashby
-- Run in Supabase SQL editor

INSERT INTO companies (name, slug, ats_type, ats_slug, careers_url, quality_score, active)
VALUES
  ('Linear',            'linear',            'ashby', 'linear',            'https://jobs.ashbyhq.com/linear',            90, true),
  ('Verkada',           'verkada',           'ashby', 'verkada',           'https://jobs.ashbyhq.com/verkada',           85, true),
  ('Rippling',          'rippling',          'ashby', 'rippling',          'https://jobs.ashbyhq.com/rippling',          88, true),
  ('1Password',         '1password',         'ashby', '1password',         'https://jobs.ashbyhq.com/1password',         87, true),
  ('Abnormal Security', 'abnormal-security', 'ashby', 'AbnormalSecurity',  'https://jobs.ashbyhq.com/AbnormalSecurity',  85, true),
  ('Notion',            'notion',            'ashby', 'notion',            'https://jobs.ashbyhq.com/notion',            88, true),
  ('Vercel',            'vercel',            'ashby', 'vercel',            'https://jobs.ashbyhq.com/vercel',            85, true),
  ('Figma',             'figma',             'ashby', 'figma',             'https://jobs.ashbyhq.com/figma',             90, true),
  ('Retool',            'retool',            'ashby', 'retool',            'https://jobs.ashbyhq.com/retool',            84, true),
  ('Brex',              'brex',              'ashby', 'brex',              'https://jobs.ashbyhq.com/brex',              83, true),
  ('Drata',             'drata',             'ashby', 'drata',             'https://jobs.ashbyhq.com/drata',             82, true),
  ('Vanta',             'vanta',             'ashby', 'vanta',             'https://jobs.ashbyhq.com/vanta',             83, true),
  ('Anthropic',         'anthropic',         'ashby', 'Anthropic',         'https://jobs.ashbyhq.com/Anthropic',         92, true),
  ('Perplexity AI',     'perplexity-ai',     'ashby', 'perplexityai',      'https://jobs.ashbyhq.com/perplexityai',      88, true),
  ('Wiz',               'wiz',               'ashby', 'wiz-security',      'https://jobs.ashbyhq.com/wiz-security',      89, true)
ON CONFLICT (slug) DO UPDATE SET
  ats_type   = EXCLUDED.ats_type,
  ats_slug   = EXCLUDED.ats_slug,
  careers_url = EXCLUDED.careers_url,
  quality_score = EXCLUDED.quality_score,
  active     = EXCLUDED.active;

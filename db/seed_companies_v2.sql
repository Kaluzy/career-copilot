-- ============================================================
-- Career Copilot — Additional Companies (v2)
-- Run in Supabase SQL Editor after seed_companies.sql
-- Adds: Healthcare, Defense IT, Financial, IT Services, Endpoint tools
-- ============================================================

INSERT INTO companies (name, slug, ats_type, ats_slug, careers_url, size, quality_score, remote_policy, industry, user_status) VALUES

-- ── Endpoint / MDM Tools (they hire IT engineers who use their own products) ──
('Jamf',                   'jamf',          'greenhouse', 'jamf',           'https://www.jamf.com/about/careers/',           'midsize',    88, 'hybrid',  'endpoint_tools',  'preferred'),
('Kandji',                 'kandji',        'greenhouse', 'kandji',         'https://kandji.io/company/careers/',            'smb',        82, 'remote',  'endpoint_tools',  'preferred'),
('Automox',                'automox',       'greenhouse', 'automox',        'https://www.automox.com/careers',               'smb',        80, 'remote',  'endpoint_tools',  'preferred'),

-- ── Healthcare IT ─────────────────────────────────────────────────────────────
('HCA Healthcare',         'hca',           'html',        null,             'https://careers.hcahealthcare.com/',            'enterprise', 80, 'hybrid',  'healthcare',      'preferred'),
('Ascension Health',       'ascension',     'html',        null,             'https://careers.ascension.org/',                'enterprise', 78, 'hybrid',  'healthcare',      'preferred'),
('CommonSpirit Health',    'commonspirit',  'html',        null,             'https://jobs.commonspirit.org/',                'enterprise', 76, 'hybrid',  'healthcare',      'preferred'),
('Mayo Clinic',            'mayo-clinic',   'html',        null,             'https://jobs.mayoclinic.org/',                  'enterprise', 90, 'hybrid',  'healthcare',      'preferred'),
('Cleveland Clinic',       'cleveland-clinic', 'html',     null,             'https://jobs.clevelandclinic.org/',             'enterprise', 88, 'hybrid',  'healthcare',      'preferred'),
('Cerner / Oracle Health', 'cerner',        'html',        null,             'https://www.oracle.com/careers/',               'enterprise', 80, 'hybrid',  'healthcare_it',   'neutral'),
('Epic Systems',           'epic',          'html',        null,             'https://careers.epic.com/',                     'midsize',    85, 'onsite',  'healthcare_it',   'neutral'),

-- ── Defense / Government IT ───────────────────────────────────────────────────
('General Dynamics IT',    'gdit',          'greenhouse', 'gdit',           'https://www.gdit.com/careers/',                 'enterprise', 82, 'hybrid',  'defense_it',      'neutral'),
('ManTech',                'mantech',       'greenhouse', 'mantech',        'https://www.mantech.com/careers/',              'midsize',    78, 'hybrid',  'defense_it',      'neutral'),
('CACI International',     'caci',          'html',        null,             'https://careers.caci.com/',                     'enterprise', 78, 'hybrid',  'defense_it',      'neutral'),
('Northrop Grumman',       'northrop',      'html',        null,             'https://www.northropgrumman.com/careers/',      'enterprise', 82, 'hybrid',  'defense_it',      'neutral'),
('Peraton',                'peraton',       'greenhouse', 'peraton',        'https://www.peraton.com/careers/',              'enterprise', 78, 'hybrid',  'defense_it',      'neutral'),

-- ── IT Services / MSP ─────────────────────────────────────────────────────────
('DXC Technology',         'dxc',           'html',        null,             'https://dxc.com/us/en/about-dxc/careers',       'enterprise', 72, 'hybrid',  'it_services',     'neutral'),
('Unisys',                 'unisys',        'html',        null,             'https://www.unisys.com/careers/',               'enterprise', 70, 'hybrid',  'it_services',     'neutral'),
('Conduent',               'conduent',      'html',        null,             'https://www.conduent.com/careers/',             'enterprise', 68, 'hybrid',  'it_services',     'neutral'),
('Accenture',              'accenture',     'html',        null,             'https://www.accenture.com/us-en/careers',       'enterprise', 80, 'hybrid',  'consulting',      'neutral'),
('Deloitte',               'deloitte',      'html',        null,             'https://jobs2.deloitte.com/us/en',              'enterprise', 82, 'hybrid',  'consulting',      'neutral'),
('Kforce',                 'kforce',        'html',        null,             'https://www.kforce.com/find-a-job/',            'midsize',    68, 'hybrid',  'staffing',        'neutral'),
('TEKsystems',             'teksystems',    'html',        null,             'https://www.teksystems.com/en/careers',         'enterprise', 70, 'hybrid',  'staffing',        'neutral'),
('SHI International',      'shi',           'html',        null,             'https://www.shi.com/careers',                   'enterprise', 78, 'hybrid',  'it_services',     'neutral'),

-- ── Financial (large IT departments) ─────────────────────────────────────────
('Wells Fargo',            'wells-fargo',   'html',        null,             'https://www.wellsfargojobs.com/',               'enterprise', 78, 'hybrid',  'financial',       'preferred'),
('Citi',                   'citi',          'html',        null,             'https://jobs.citi.com/',                        'enterprise', 78, 'hybrid',  'financial',       'preferred'),
('Goldman Sachs',          'goldman-sachs', 'html',        null,             'https://www.goldmansachs.com/careers/',         'enterprise', 85, 'hybrid',  'financial',       'neutral'),
('Morgan Stanley',         'morgan-stanley','html',        null,             'https://www.morganstanley.com/careers',         'enterprise', 85, 'hybrid',  'financial',       'neutral'),
('American Express',       'amex',          'html',        null,             'https://jobs.americanexpress.com/',             'enterprise', 82, 'hybrid',  'financial',       'preferred'),
('Vanguard',               'vanguard',      'html',        null,             'https://www.vanguardjobs.com/',                 'enterprise', 80, 'remote',  'financial',       'preferred'),

-- ── Cloud / SaaS (strong IT infra teams) ──────────────────────────────────────
('Atlassian',              'atlassian',     'greenhouse', 'atlassian',      'https://www.atlassian.com/company/careers',     'enterprise', 90, 'remote',  'saas',            'preferred'),
('Zoom',                   'zoom',          'greenhouse', 'zoom',           'https://careers.zoom.us/',                      'enterprise', 85, 'remote',  'saas',            'neutral'),
('Dropbox',                'dropbox',       'greenhouse', 'dropbox',        'https://jobs.dropbox.com/',                     'midsize',    82, 'remote',  'saas',            'neutral'),
('Box',                    'box',           'greenhouse', 'boxinc',         'https://careers.box.com/',                      'midsize',    80, 'hybrid',  'saas',            'neutral'),
('HubSpot',                'hubspot',       'greenhouse', 'hubspot',        'https://www.hubspot.com/careers',               'enterprise', 88, 'hybrid',  'saas',            'neutral'),
('Stripe',                 'stripe',        'greenhouse', 'stripe',         'https://stripe.com/jobs',                       'enterprise', 90, 'hybrid',  'fintech',         'neutral'),
('Twilio',                 'twilio2',       'greenhouse', 'twilio',         'https://www.twilio.com/en-us/company/jobs',     'enterprise', 82, 'remote',  'saas',            'neutral'),
('HashiCorp',              'hashicorp2',    'greenhouse', 'hashicorp',      'https://www.hashicorp.com/jobs',                'midsize',    85, 'remote',  'devtools',        'neutral')

ON CONFLICT (slug) DO NOTHING;

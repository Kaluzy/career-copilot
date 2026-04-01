-- ============================================================
-- Career Copilot — Company Registry Seed
-- 50 target companies for IT endpoint/sysadmin/EUC roles
-- Run AFTER schema.sql
-- ============================================================

INSERT INTO companies (name, slug, ats_type, ats_slug, ats_url, careers_url, size, quality_score, remote_policy, industry, hq_location, notes, user_status) VALUES

-- ── Greenhouse companies (structured API, easiest to ingest) ──

('Cloudflare', 'cloudflare', 'greenhouse', 'cloudflare',
  'https://boards-api.greenhouse.io/v1/boards/cloudflare/jobs',
  'https://www.cloudflare.com/careers/', 'enterprise', 88, 'hybrid', 'tech', 'San Francisco, CA',
  'Strong endpoint + IT ops roles. Good remote options.', 'preferred'),

('Okta', 'okta', 'greenhouse', 'okta',
  'https://boards-api.greenhouse.io/v1/boards/okta/jobs',
  'https://www.okta.com/company/careers/', 'enterprise', 85, 'hybrid', 'tech', 'San Francisco, CA',
  'Identity/security company. IT operations and endpoint roles.', 'preferred'),

('CrowdStrike', 'crowdstrike', 'greenhouse', 'crowdstrike',
  'https://boards-api.greenhouse.io/v1/boards/crowdstrike/jobs',
  'https://www.crowdstrike.com/careers/', 'enterprise', 87, 'remote', 'security', 'Austin, TX',
  'Cybersecurity. IT support engineer roles. Good growth path.', 'preferred'),

('Datadog', 'datadog', 'greenhouse', 'datadog',
  'https://boards-api.greenhouse.io/v1/boards/datadog/jobs',
  'https://www.datadoghq.com/careers/', 'enterprise', 84, 'hybrid', 'tech', 'New York, NY',
  'Observability/monitoring. IT ops and endpoint roles.', 'neutral'),

('Rapid7', 'rapid7', 'greenhouse', 'rapid7',
  'https://boards-api.greenhouse.io/v1/boards/rapid7/jobs',
  'https://www.rapid7.com/careers/', 'midsize', 80, 'hybrid', 'security', 'Boston, MA',
  'Security company. IT support and endpoint engineering roles.', 'neutral'),

('Twilio', 'twilio', 'greenhouse', 'twilio',
  'https://boards-api.greenhouse.io/v1/boards/twilio/jobs',
  'https://www.twilio.com/en-us/company/jobs', 'enterprise', 78, 'remote', 'tech', 'San Francisco, CA',
  'Communications platform. IT ops roles. Remote-friendly.', 'neutral'),

('HashiCorp', 'hashicorp', 'greenhouse', 'hashicorp',
  'https://boards-api.greenhouse.io/v1/boards/hashicorp/jobs',
  'https://www.hashicorp.com/careers', 'midsize', 82, 'remote', 'tech', 'San Francisco, CA',
  'Infrastructure/automation tooling. Good for sysadmin-track.', 'neutral'),

('Figma', 'figma', 'greenhouse', 'figma',
  'https://boards-api.greenhouse.io/v1/boards/figma/jobs',
  'https://www.figma.com/careers/', 'midsize', 80, 'hybrid', 'tech', 'San Francisco, CA',
  'Design tools company. Corporate IT and endpoint roles.', 'neutral'),

('Brex', 'brex', 'greenhouse', 'brex',
  'https://boards-api.greenhouse.io/v1/boards/brex/jobs',
  'https://www.brex.com/careers', 'midsize', 76, 'remote', 'fintech', 'San Francisco, CA',
  'Fintech. IT engineering roles.', 'neutral'),

('Palantir', 'palantir', 'greenhouse', 'palantir',
  'https://boards-api.greenhouse.io/v1/boards/palantir/jobs',
  'https://www.palantir.com/careers/', 'enterprise', 75, 'hybrid', 'tech', 'Denver, CO',
  'Data analytics. Technical support and IT roles.', 'neutral'),

-- ── Lever companies ──────────────────────────────────────

('Procore', 'procore', 'lever', 'procore',
  'https://api.lever.co/v0/postings/procore?mode=json',
  'https://www.procore.com/jobs', 'midsize', 78, 'hybrid', 'tech', 'Carpinteria, CA',
  'Construction tech. IT support and endpoint roles.', 'neutral'),

('Gusto', 'gusto', 'lever', 'gusto',
  'https://api.lever.co/v0/postings/gusto?mode=json',
  'https://gusto.com/about/careers', 'midsize', 79, 'remote', 'hr_tech', 'San Francisco, CA',
  'HR/payroll platform. IT operations roles. Remote-friendly.', 'neutral'),

('Etsy', 'etsy', 'lever', 'etsy',
  'https://api.lever.co/v0/postings/etsy?mode=json',
  'https://careers.etsy.com/', 'enterprise', 76, 'hybrid', 'ecommerce', 'Brooklyn, NY',
  'Ecommerce marketplace. Corporate IT and sysadmin roles.', 'neutral'),

('Squarespace', 'squarespace', 'lever', 'squarespace',
  'https://api.lever.co/v0/postings/squarespace?mode=json',
  'https://www.squarespace.com/about/careers', 'midsize', 75, 'hybrid', 'tech', 'New York, NY',
  'Website platform. Corporate IT and endpoint roles.', 'neutral'),

('Asana', 'asana', 'lever', 'asana',
  'https://api.lever.co/v0/postings/asana?mode=json',
  'https://asana.com/jobs', 'midsize', 78, 'hybrid', 'tech', 'San Francisco, CA',
  'Project management platform. IT support and endpoint.', 'neutral'),

-- ── Ashby companies ──────────────────────────────────────

('Notion', 'notion', 'ashby', 'notion',
  'https://jobs.ashbyhq.com/notion/non-applied/job-board-api',
  'https://www.notion.so/careers', 'midsize', 79, 'hybrid', 'tech', 'San Francisco, CA',
  'Productivity platform. IT ops roles.', 'neutral'),

('Vercel', 'vercel', 'ashby', 'vercel',
  'https://jobs.ashbyhq.com/vercel/non-applied/job-board-api',
  'https://vercel.com/careers', 'midsize', 77, 'remote', 'tech', 'San Francisco, CA',
  'Dev platform. IT roles. Fully remote.', 'neutral'),

-- ── Workday / HTML companies (need scraper — lower priority) ──

('Microsoft', 'microsoft', 'workday', null,
  null,
  'https://careers.microsoft.com/', 'enterprise', 95, 'hybrid', 'tech', 'Redmond, WA',
  'Top target. Endpoint, sysadmin, EUC, MDM roles. SCCM/Intune home turf.', 'preferred'),

('Google', 'google', 'html', null,
  null,
  'https://careers.google.com/', 'enterprise', 93, 'hybrid', 'tech', 'Mountain View, CA',
  'IT Specialist and Corporate Engineering roles. Competitive but worth monitoring.', 'preferred'),

('Amazon', 'amazon', 'html', null,
  null,
  'https://www.amazon.jobs/', 'enterprise', 82, 'hybrid', 'tech', 'Seattle, WA',
  'IT support, endpoint, and systems roles. High volume.', 'neutral'),

('Dell Technologies', 'dell', 'html', null,
  null,
  'https://jobs.dell.com/', 'enterprise', 83, 'hybrid', 'tech', 'Round Rock, TX',
  'Endpoint mgmt, deployment, EUC roles. Good career path.', 'preferred'),

('HP Inc', 'hp', 'html', null,
  null,
  'https://jobs.hp.com/', 'enterprise', 80, 'hybrid', 'tech', 'Palo Alto, CA',
  'Endpoint and device management roles.', 'neutral'),

('Cisco', 'cisco', 'workday', null,
  null,
  'https://jobs.cisco.com/', 'enterprise', 88, 'hybrid', 'tech', 'San Jose, CA',
  'IT support engineer, endpoint, and infrastructure roles. Strong growth path.', 'preferred'),

('ServiceNow', 'servicenow', 'workday', null,
  null,
  'https://careers.servicenow.com/', 'enterprise', 90, 'hybrid', 'tech', 'Santa Clara, CA',
  'IT platform company. Good IT operations and endpoint roles internally.', 'preferred'),

('Salesforce', 'salesforce', 'workday', null,
  null,
  'https://careers.salesforce.com/', 'enterprise', 88, 'hybrid', 'tech', 'San Francisco, CA',
  'Enterprise software. IT support and endpoint roles.', 'neutral'),

('VMware / Broadcom', 'vmware', 'html', null,
  null,
  'https://careers.broadcom.com/', 'enterprise', 78, 'hybrid', 'tech', 'Palo Alto, CA',
  'Virtualization and endpoint management. Workspace ONE (MDM) home.', 'preferred'),

('Ivanti', 'ivanti', 'greenhouse', 'ivanti',
  'https://boards-api.greenhouse.io/v1/boards/ivanti/jobs',
  'https://www.ivanti.com/company/careers', 'midsize', 79, 'hybrid', 'tech', 'South Jordan, UT',
  'Endpoint management software company. Patch/UEM/MDM. Strong fit.', 'preferred'),

('Tanium', 'tanium', 'greenhouse', 'tanium',
  'https://boards-api.greenhouse.io/v1/boards/tanium/jobs',
  'https://www.tanium.com/careers/', 'midsize', 82, 'hybrid', 'security', 'Kirkland, WA',
  'Endpoint security/management platform. IT roles at a company that builds these tools.', 'preferred'),

('Absolute Security', 'absolute', 'greenhouse', 'absolutesoftware',
  'https://boards-api.greenhouse.io/v1/boards/absolutesoftware/jobs',
  'https://www.absolute.com/company/careers/', 'smb', 72, 'hybrid', 'security', 'Vancouver, BC',
  'Endpoint security. IT roles.', 'neutral'),

-- ── MSP / VAR companies (good for endpoint experience) ────

('CDW', 'cdw', 'html', null,
  null,
  'https://careers.cdw.com/', 'enterprise', 78, 'hybrid', 'it_services', 'Vernon Hills, IL',
  'IT solutions provider. Deployment, endpoint, sysadmin roles. High volume hiring.', 'preferred'),

('Insight Direct', 'insight', 'html', null,
  null,
  'https://careers.insight.com/', 'enterprise', 74, 'hybrid', 'it_services', 'Tempe, AZ',
  'IT solutions. Field endpoint and deployment roles.', 'neutral'),

('World Wide Technology', 'wwt', 'greenhouse', 'wwt',
  'https://boards-api.greenhouse.io/v1/boards/wwt/jobs',
  'https://www.wwt.com/careers', 'enterprise', 80, 'hybrid', 'it_services', 'St. Louis, MO',
  'IT solutions. Good endpoint and infrastructure roles.', 'neutral'),

('Presidio', 'presidio', 'greenhouse', 'presidio',
  'https://boards-api.greenhouse.io/v1/boards/presidio/jobs',
  'https://www.presidio.com/careers/', 'midsize', 76, 'hybrid', 'it_services', 'New York, NY',
  'IT solutions and managed services. Endpoint deployment roles.', 'neutral'),

-- ── Healthcare IT companies (relevant background match) ──

('Optum (UnitedHealth)', 'optum', 'html', null,
  null,
  'https://careers.unitedhealthgroup.com/', 'enterprise', 83, 'hybrid', 'healthcare_it', 'Eden Prairie, MN',
  'Healthcare IT giant. Endpoint, sysadmin, EUC roles. Healthcare background = advantage.', 'preferred'),

('CVS Health', 'cvs', 'html', null,
  null,
  'https://jobs.cvshealth.com/', 'enterprise', 80, 'hybrid', 'healthcare', 'Woonsocket, RI',
  'Healthcare + pharmacy. IT support and endpoint roles. Healthcare background helps.', 'preferred'),

('Epic Systems', 'epic', 'html', null,
  null,
  'https://www.epic.com/careers', 'midsize', 82, 'hybrid', 'healthcare_it', 'Verona, WI',
  'EHR software. IT and technical roles. Healthcare experience relevant.', 'neutral'),

('Cerner / Oracle Health', 'oracle-health', 'html', null,
  null,
  'https://www.oracle.com/careers/', 'enterprise', 78, 'hybrid', 'healthcare_it', 'Kansas City, MO',
  'Healthcare IT. Endpoint and systems roles.', 'neutral'),

('Kaiser Permanente', 'kaiser', 'html', null,
  null,
  'https://jobs.kaiserpermanente.org/', 'enterprise', 85, 'hybrid', 'healthcare', 'Oakland, CA',
  'Large healthcare provider. Strong IT department. Good sysadmin and EUC roles.', 'preferred'),

-- ── Financial/Insurance (good IT structure) ──────────────

('Capital One', 'capitalone', 'greenhouse', 'capitalone',
  'https://boards-api.greenhouse.io/v1/boards/capitalone/jobs',
  'https://www.capitalonecareers.com/', 'enterprise', 84, 'hybrid', 'finance', 'McLean, VA',
  'Tech-forward bank. IT support engineer and endpoint roles. Strong engineering path.', 'preferred'),

('Fidelity Investments', 'fidelity', 'html', null,
  null,
  'https://jobs.fidelity.com/', 'enterprise', 85, 'hybrid', 'finance', 'Boston, MA',
  'Large financial services. Excellent IT structure. Sysadmin and endpoint roles.', 'preferred'),

('Nationwide Insurance', 'nationwide', 'html', null,
  null,
  'https://jobs.nationwide.com/', 'enterprise', 78, 'hybrid', 'insurance', 'Columbus, OH',
  'Insurance company. Endpoint and IT operations roles. Stable employer.', 'neutral'),

-- ── Government/Defense (stable, sysadmin path) ───────────

('SAIC', 'saic', 'html', null,
  null,
  'https://jobs.saic.com/', 'enterprise', 78, 'hybrid', 'defense', 'Reston, VA',
  'Government IT contractor. Sysadmin and endpoint roles. Clearance may be required for some.', 'neutral'),

('Leidos', 'leidos', 'html', null,
  null,
  'https://careers.leidos.com/', 'enterprise', 77, 'hybrid', 'defense', 'Reston, VA',
  'Government IT. Systems administrator and IT support roles. Stable.', 'neutral'),

('Booz Allen Hamilton', 'booz-allen', 'greenhouse', 'boozallen',
  'https://boards-api.greenhouse.io/v1/boards/boozallen/jobs',
  'https://www.boozallen.com/careers.html', 'enterprise', 79, 'hybrid', 'consulting', 'McLean, VA',
  'Consulting + government IT. Sysadmin and endpoint roles.', 'neutral'),

-- ── Large General Employers (high IT headcount) ──────────

('Target Corporation', 'target', 'html', null,
  null,
  'https://jobs.target.com/', 'enterprise', 78, 'hybrid', 'retail', 'Minneapolis, MN',
  'Large retailer. Internal IT and endpoint roles. Underrated tech employer.', 'neutral'),

('JPMorgan Chase', 'jpmorgan', 'html', null,
  null,
  'https://careers.jpmorgan.com/', 'enterprise', 85, 'hybrid', 'finance', 'New York, NY',
  'Largest US bank. IT operations, endpoint, and sysadmin roles. Excellent structure.', 'preferred'),

('Bank of America', 'bofa', 'html', null,
  null,
  'https://careers.bankofamerica.com/', 'enterprise', 83, 'hybrid', 'finance', 'Charlotte, NC',
  'Major bank. IT support and endpoint roles. Large IT department.', 'neutral'),

-- ── Security companies (endpoint security overlap) ────────

('Palo Alto Networks', 'palo-alto', 'greenhouse', 'paloaltonetworks',
  'https://boards-api.greenhouse.io/v1/boards/paloaltonetworks/jobs',
  'https://www.paloaltonetworks.com/company/careers', 'enterprise', 87, 'hybrid', 'security', 'Santa Clara, CA',
  'Cybersecurity. IT support engineer and endpoint roles. Good career path.', 'preferred'),

('Fortinet', 'fortinet', 'greenhouse', 'fortinet',
  'https://boards-api.greenhouse.io/v1/boards/fortinet/jobs',
  'https://www.fortinet.com/corporate/about-us/careers.html', 'enterprise', 82, 'hybrid', 'security', 'Sunnyvale, CA',
  'Network security. Technical support and IT operations roles.', 'neutral'),

('SentinelOne', 'sentinelone', 'greenhouse', 'sentinelone',
  'https://boards-api.greenhouse.io/v1/boards/sentinelone/jobs',
  'https://www.sentinelone.com/careers/', 'midsize', 81, 'remote', 'security', 'Mountain View, CA',
  'Endpoint security. IT support and technical roles. Remote-friendly.', 'preferred')

ON CONFLICT (slug) DO NOTHING;

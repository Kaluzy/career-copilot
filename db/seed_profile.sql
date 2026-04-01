-- ============================================================
-- Career Copilot — Candidate Profile Seed
-- Run AFTER creating your account in the app
-- Replace 'YOUR-USER-UUID-HERE' with your Supabase auth user ID
-- (Find it in Supabase Dashboard → Authentication → Users)
-- ============================================================

INSERT INTO candidate_profile (
  user_id,
  full_name,
  current_title,
  current_company,
  years_experience,
  skills,
  tools,
  target_roles,
  target_titles,
  avoid_roles,
  salary_min,
  salary_target,
  locations,
  remote_pref,
  work_auth,
  career_summary
) VALUES (
  'YOUR-USER-UUID-HERE',
  'Kaleab Tesfaye',
  'Desktop Support Specialist',
  'Maxim Healthcare',
  4,

  -- Skills: [{skill, level (1-5), years_exp}]
  '[
    {"skill": "Windows 10/11 endpoint support", "level": 5, "years_exp": 4},
    {"skill": "Hardware troubleshooting", "level": 5, "years_exp": 4},
    {"skill": "Software deployment and packaging", "level": 4, "years_exp": 3},
    {"skill": "Microsoft Intune / MDM", "level": 3, "years_exp": 2},
    {"skill": "SCCM / Microsoft Endpoint Configuration Manager", "level": 3, "years_exp": 2},
    {"skill": "Active Directory / Group Policy", "level": 4, "years_exp": 3},
    {"skill": "PowerShell scripting", "level": 3, "years_exp": 2},
    {"skill": "Device lifecycle management", "level": 4, "years_exp": 3},
    {"skill": "Remote support tools (TeamViewer, RDP)", "level": 5, "years_exp": 4},
    {"skill": "ServiceNow ticketing", "level": 5, "years_exp": 4},
    {"skill": "Windows imaging and deployment", "level": 4, "years_exp": 3},
    {"skill": "Office 365 / Microsoft 365 administration", "level": 4, "years_exp": 3},
    {"skill": "Network troubleshooting (TCP/IP, DNS, DHCP)", "level": 3, "years_exp": 3},
    {"skill": "Printer and peripheral support", "level": 5, "years_exp": 4},
    {"skill": "Virtualization basics (VMware, Hyper-V)", "level": 2, "years_exp": 1},
    {"skill": "Android MDM / Samsung Knox", "level": 3, "years_exp": 2},
    {"skill": "iOS device management", "level": 3, "years_exp": 2},
    {"skill": "Endpoint security concepts", "level": 3, "years_exp": 2}
  ]',

  -- Tools
  '[
    {"tool": "Microsoft Intune", "proficiency": "intermediate"},
    {"tool": "SCCM / ConfigMgr", "proficiency": "intermediate"},
    {"tool": "ServiceNow", "proficiency": "advanced"},
    {"tool": "Active Directory", "proficiency": "intermediate"},
    {"tool": "PowerShell", "proficiency": "intermediate"},
    {"tool": "Microsoft 365 Admin Center", "proficiency": "intermediate"},
    {"tool": "Autopilot / Windows Autopilot", "proficiency": "beginner"},
    {"tool": "Tanium", "proficiency": "beginner"},
    {"tool": "Zscaler", "proficiency": "beginner"},
    {"tool": "Remote Desktop / RDP", "proficiency": "advanced"},
    {"tool": "TeamViewer", "proficiency": "advanced"},
    {"tool": "Jamf", "proficiency": "none"},
    {"tool": "Azure AD", "proficiency": "beginner"}
  ]',

  -- Target roles (categories from schema)
  ARRAY['endpoint_management', 'digital_workplace', 'systems_admin', 'mdm_mobility', 'desktop_engineering', 'it_operations'],

  -- Target titles (for scoring and search)
  ARRAY[
    'Endpoint Administrator',
    'Endpoint Management Specialist',
    'Endpoint Engineer',
    'Endpoint Operations Analyst',
    'Endpoint Specialist',
    'Systems Administrator',
    'Desktop Engineer',
    'Digital Workplace Specialist',
    'Digital Workplace Engineer',
    'EUC Engineer',
    'MDM Engineer',
    'Mobility Engineer',
    'Workplace Technology Specialist',
    'Technical Support Engineer',
    'IT Operations Analyst',
    'Infrastructure Support Engineer',
    'Application Deployment Specialist',
    'Desktop Engineering Specialist'
  ]',

  -- Roles to avoid
  ARRAY['help_desk_tier1', 'sales_engineering', 'software_development', 'data_science'],

  65000,   -- salary minimum (adjust to your actual floor)
  85000,   -- salary target (adjust to your goal)

  ARRAY['Remote', 'United States'],
  'preferred',    -- remote preference
  'us_citizen',

  'IT support professional with 4+ years of experience in endpoint management, device deployment, and user support across Windows enterprise environments. Skilled in Intune MDM, SCCM, Active Directory, PowerShell scripting, and device lifecycle management in regulated healthcare settings. Seeking to grow into a dedicated endpoint operations, systems administration, or digital workplace engineering role.'
)
ON CONFLICT DO NOTHING;

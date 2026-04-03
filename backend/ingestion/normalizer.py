"""
Normalize raw job data from any ATS into the standard jobs schema.
"""
import re
import hashlib
from datetime import date
from bs4 import BeautifulSoup


# ── Role category mapping ─────────────────────────────────────────────────────
ROLE_KEYWORDS: dict[str, list[str]] = {
    "endpoint_management": [
        "endpoint management", "endpoint administrator", "endpoint admin",
        "endpoint specialist", "endpoint engineer", "endpoint operations",
        "endpoint analyst", "client management", "client engineer",
        "euc", "end user computing", "endpoint support", "unified endpoint"
    ],
    "digital_workplace": [
        "digital workplace", "workplace technology", "workplace specialist",
        "workplace engineer", "digital workplace engineer", "workplace support",
        "dex", "digital employee experience"
    ],
    "systems_admin": [
        "systems administrator", "sysadmin", "system administrator",
        "systems admin", "windows administrator", "windows admin",
        "infrastructure administrator", "it administrator", "server administrator"
    ],
    "mdm_mobility": [
        "mdm", "mobile device management", "mobility engineer", "mobility specialist",
        "jamf", "intune engineer", "mobile management", "uem engineer",
        "unified endpoint management"
    ],
    "desktop_engineering": [
        "desktop engineer", "desktop engineering", "desktop administrator",
        "desktop analyst", "desktop deployment", "field engineer",
        "field technician", "deskside"
    ],
    "deployment_packaging": [
        "deployment specialist", "application packaging", "app deployment",
        "software deployment", "sccm engineer", "configuration manager",
        "packaging engineer", "software packaging", "app packager"
    ],
    "it_operations": [
        "it operations", "it ops", "operations analyst", "infrastructure support",
        "it support engineer", "technical support engineer", "platform support",
        "it infrastructure", "corporate it", "saas administrator", "saas admin",
        "it engineer", "corporate technology", "workplace engineer",
        "it generalist", "systems support", "technology support engineer",
        "technology operations", "it specialist"
    ],
    "help_desk": [
        "help desk", "helpdesk", "service desk", "desktop support", "level 1",
        "level 2", "tier 1", "tier 2", "it support specialist", "it technician",
        "it support analyst", "support analyst", "user support"
    ],
}

# Role category → growth tier (used in growth_fit scoring)
GROWTH_TIER: dict[str, str] = {
    "endpoint_management": "target",     # ideal destination
    "digital_workplace":   "target",
    "systems_admin":       "target",
    "mdm_mobility":        "target",
    "desktop_engineering": "aligned",    # good step
    "deployment_packaging":"aligned",
    "it_operations":       "aligned",
    "help_desk":           "lateral",    # no growth
}

# Seniority signals
SENIOR_WORDS = ["senior", "sr.", "lead", "principal", "staff", "manager", "director"]
JUNIOR_WORDS = ["junior", "jr.", "entry", "associate", "level i", "tier i", "level 1"]


def categorize_role(title: str) -> str:
    title_lower = title.lower()
    for category, keywords in ROLE_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                return category
    return "other"


# Only store jobs in these categories — drop everything else before hitting the DB
KEEP_CATEGORIES = {
    "endpoint_management", "digital_workplace", "systems_admin",
    "mdm_mobility", "desktop_engineering", "deployment_packaging",
    "it_operations", "help_desk",
}


def is_relevant(role_category: str) -> bool:
    """Return True if this job is worth storing and scoring."""
    return role_category in KEEP_CATEGORIES


def detect_seniority(title: str) -> str:
    title_lower = title.lower()
    for w in SENIOR_WORDS:
        if w in title_lower:
            return "senior"
    for w in JUNIOR_WORDS:
        if w in title_lower:
            return "junior"
    return "mid"


def detect_remote(location: str, description: str) -> tuple[bool, bool]:
    """Returns (remote, hybrid)"""
    text = (location + " " + description).lower()
    is_remote = any(w in text for w in ["remote", "work from home", "wfh", "fully remote"])
    is_hybrid = any(w in text for w in ["hybrid", "flexible", "partially remote"])
    if is_remote and is_hybrid:
        is_remote = False  # hybrid takes priority if both detected
    return is_remote, is_hybrid


def extract_salary(description: str) -> tuple[int | None, int | None]:
    """Try to extract salary range from job description text."""
    patterns = [
        r'\$(\d{2,3}(?:,\d{3})?(?:\.\d+)?)[Kk]?\s*[-–—to]+\s*\$?(\d{2,3}(?:,\d{3})?(?:\.\d+)?)[Kk]?',
        r'(\d{2,3}(?:,\d{3})?)\s*[-–—to]+\s*(\d{2,3}(?:,\d{3})?)\s*(?:per year|annually|\/yr|\/year)',
    ]
    for pattern in patterns:
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            low = float(match.group(1).replace(",", ""))
            high = float(match.group(2).replace(",", ""))
            # If values look like thousands (e.g., "85K"), multiply
            if low < 500:
                low *= 1000
                high *= 1000
            return int(low), int(high)
    return None, None


def clean_html(html: str) -> str:
    """Strip HTML tags, normalize whitespace."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def make_source_id(ats_type: str, company_slug: str, job_id: str) -> str:
    """Stable dedup key."""
    raw = f"{ats_type}:{company_slug}:{job_id}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def normalize_job(
    raw: dict,
    company_id: str,
    company_slug: str,
    ats_type: str,
) -> dict:
    """
    Convert a raw ATS job dict to the standard jobs schema dict.
    Each connector calls this after extracting its fields.
    """
    title = raw.get("title", "Unknown")
    description_raw = raw.get("description_raw", "")
    description_clean = clean_html(description_raw)
    location = raw.get("location", "")

    remote, hybrid = detect_remote(location, description_clean)
    salary_min, salary_max = extract_salary(description_clean)
    # Connector-provided salary overrides extracted
    if raw.get("salary_min"):
        salary_min = raw["salary_min"]
    if raw.get("salary_max"):
        salary_max = raw["salary_max"]

    role_category = categorize_role(title)
    seniority = detect_seniority(title)
    source_id = make_source_id(ats_type, company_slug, str(raw.get("job_id", "")))

    return {
        "company_id": company_id,
        "source_id": source_id,
        "source": ats_type,
        "title": title,
        "description_raw": description_raw[:50000],   # cap size
        "description_clean": description_clean[:20000],
        "location": location,
        "remote": remote,
        "hybrid": hybrid,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "role_category": role_category,
        "seniority": seniority,
        "posted_at": raw.get("posted_at"),
        "apply_url": raw.get("apply_url", ""),
        "status": "new",
    }

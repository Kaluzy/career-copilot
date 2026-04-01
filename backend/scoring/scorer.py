"""
Fit scoring engine — MVP rule-based version.
Scores a job against the candidate profile across 7 dimensions.
Phase 2 will add Claude AI for rationale generation.
"""
from ingestion.normalizer import ROLE_KEYWORDS, GROWTH_TIER


# ── Weights (must sum to 1.0) ─────────────────────────────────────────────────
WEIGHTS = {
    "role_fit":        0.30,
    "growth_fit":      0.20,
    "skills_match":    0.20,
    "comp_fit":        0.10,
    "remote_fit":      0.10,
    "company_quality": 0.05,
    "realism":         0.05,
}

# Job categories that are direct targets vs stretch
TARGET_CATEGORIES  = {"endpoint_management", "digital_workplace", "systems_admin", "mdm_mobility"}
ALIGNED_CATEGORIES = {"desktop_engineering", "deployment_packaging", "it_operations"}
LATERAL_CATEGORIES = {"help_desk"}


def score_role_fit(job: dict, profile: dict) -> tuple[int, str]:
    """How well does the job role match the candidate's target roles?"""
    category = job.get("role_category", "other")
    title = (job.get("title") or "").lower()
    target_titles = [t.lower() for t in (profile.get("target_titles") or [])]

    # Exact/close title match is highest signal
    for target in target_titles:
        if target in title or title in target:
            return 95, f"Title '{job['title']}' matches target '{target}'"

    if category in TARGET_CATEGORIES:
        return 85, f"Role category '{category}' is a primary target"
    if category in ALIGNED_CATEGORIES:
        return 65, f"Role category '{category}' is aligned but not primary target"
    if category in LATERAL_CATEGORIES:
        return 25, f"Role category '{category}' is lateral — no growth"
    return 40, f"Role category '{category}' is unclear fit"


def score_growth_fit(job: dict) -> tuple[int, str]:
    """Does this role represent forward career movement?"""
    category = job.get("role_category", "other")
    seniority = job.get("seniority", "mid")
    growth_tier = GROWTH_TIER.get(category, "unknown")

    if growth_tier == "target" and seniority in ("mid", "senior"):
        return 90, "Target role at appropriate seniority level"
    if growth_tier == "target" and seniority == "junior":
        return 60, "Target role but junior level — slight step back"
    if growth_tier == "aligned" and seniority in ("mid", "senior"):
        return 70, "Aligned role — good step in right direction"
    if growth_tier == "lateral":
        return 20, "Lateral move — no growth value"
    return 50, "Growth fit unclear"


def score_skills_match(job: dict, profile: dict) -> tuple[int, str]:
    """What percentage of job keywords match candidate's skills?"""
    description = (job.get("description_clean") or "").lower()
    title = (job.get("title") or "").lower()
    text = description + " " + title

    if not text.strip():
        return 50, "No description to match against"

    candidate_skills = [
        s.get("skill", "").lower()
        for s in (profile.get("skills") or [])
    ] + [
        t.get("tool", "").lower()
        for t in (profile.get("tools") or [])
    ]

    if not candidate_skills:
        return 50, "No candidate skills defined yet"

    # Count how many candidate skills appear in the job description
    matched = [s for s in candidate_skills if s and s in text]
    match_pct = len(matched) / len(candidate_skills)

    if match_pct >= 0.7:
        score = 90
    elif match_pct >= 0.5:
        score = 75
    elif match_pct >= 0.3:
        score = 55
    elif match_pct >= 0.15:
        score = 35
    else:
        score = 15

    top_matches = matched[:5]
    note = f"{len(matched)}/{len(candidate_skills)} skills matched"
    if top_matches:
        note += f" ({', '.join(top_matches[:3])})"
    return score, note


def score_comp_fit(job: dict, profile: dict) -> tuple[int, str]:
    """Does the salary range align with the candidate's target?"""
    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")
    target = profile.get("salary_target") or 85000
    floor = profile.get("salary_min") or 65000

    if not salary_max and not salary_min:
        return 55, "Salary not listed — assuming neutral"

    effective_max = salary_max or salary_min
    effective_min = salary_min or (salary_max * 0.8 if salary_max else 0)

    if effective_max < floor:
        return 15, f"Max salary ${effective_max:,} is below your floor ${floor:,}"
    if effective_max >= target:
        return 95, f"Salary range ${effective_min:,}–${effective_max:,} meets/exceeds target"
    if effective_max >= floor:
        ratio = (effective_max - floor) / max(target - floor, 1)
        score = int(40 + ratio * 50)
        return score, f"Salary ${effective_min:,}–${effective_max:,} is below target but above floor"
    return 30, f"Salary range is low"


def score_remote_fit(job: dict, profile: dict) -> tuple[int, str]:
    """Does the remote/location setup match the candidate's preference?"""
    remote_pref = profile.get("remote_pref", "preferred")
    is_remote = job.get("remote", False)
    is_hybrid = job.get("hybrid", False)
    location = (job.get("location") or "").lower()

    # Override detection: check location field for clues
    if not is_remote and not is_hybrid:
        if "remote" in location:
            is_remote = True
        elif "hybrid" in location:
            is_hybrid = True

    if remote_pref == "required":
        if is_remote:
            return 100, "Remote role — matches requirement"
        if is_hybrid:
            return 50, "Hybrid role — partially meets remote requirement"
        return 10, "Onsite role — does not meet remote requirement"

    if remote_pref == "preferred":
        if is_remote:
            return 100, "Remote role — matches preference"
        if is_hybrid:
            return 80, "Hybrid — close to preference"
        return 45, "Onsite only — not preferred but possible"

    # "open" — location flexible
    return 70, "Location is flexible"


def score_company_quality(company: dict) -> tuple[int, str]:
    """Company quality based on quality_score in registry."""
    score = company.get("quality_score", 70)
    user_status = company.get("user_status", "neutral")

    if user_status == "blocked":
        return 0, "Company is blocked"
    if user_status == "preferred":
        score = min(score + 10, 100)
        return score, f"Preferred company (quality: {score})"
    return score, f"Company quality score: {score}"


def score_realism(job: dict) -> tuple[int, str]:
    """How realistic is it to get an interview based on seniority?"""
    seniority = job.get("seniority", "mid")
    # For a mid-level IT professional targeting growth:
    if seniority == "junior":
        return 75, "Junior role — slightly overqualified, but acceptable"
    if seniority == "mid":
        return 90, "Mid-level role — realistic match"
    if seniority == "senior":
        return 55, "Senior role — stretch, but realistic with strong application"
    if seniority == "lead":
        return 30, "Lead role — significant stretch"
    return 70, "Seniority unclear — assuming mid-level"


def score_job(job: dict, profile: dict, company: dict) -> dict:
    """
    Score a single job against the candidate profile.
    Returns a dict matching the fit_scores table schema.
    """
    # Company blocked? Skip entirely.
    if company.get("user_status") == "blocked":
        return {
            "role_fit": 0, "growth_fit": 0, "skills_match": 0,
            "comp_fit": 0, "remote_fit": 0, "company_quality": 0, "realism": 0,
            "composite": 0, "tier": "pass",
            "rationale": "Company is blocked by user."
        }

    role_fit,        role_note        = score_role_fit(job, profile)
    growth_fit,      growth_note      = score_growth_fit(job)
    skills_match,    skills_note      = score_skills_match(job, profile)
    comp_fit,        comp_note        = score_comp_fit(job, profile)
    remote_fit,      remote_note      = score_remote_fit(job, profile)
    company_quality, company_note     = score_company_quality(company)
    realism,         realism_note     = score_realism(job)

    composite = int(
        role_fit        * WEIGHTS["role_fit"]        +
        growth_fit      * WEIGHTS["growth_fit"]       +
        skills_match    * WEIGHTS["skills_match"]     +
        comp_fit        * WEIGHTS["comp_fit"]         +
        remote_fit      * WEIGHTS["remote_fit"]       +
        company_quality * WEIGHTS["company_quality"]  +
        realism         * WEIGHTS["realism"]
    )

    if composite >= 80:
        tier = "strong_fit"
    elif composite >= 65:
        tier = "good_fit"
    elif composite >= 50:
        tier = "stretch"
    else:
        tier = "pass"

    rationale = (
        f"Role: {role_note}. "
        f"Growth: {growth_note}. "
        f"Skills: {skills_note}. "
        f"Comp: {comp_note}. "
        f"Remote: {remote_note}. "
        f"Company: {company_note}. "
        f"Realism: {realism_note}."
    )

    return {
        "role_fit":        role_fit,
        "growth_fit":      growth_fit,
        "skills_match":    skills_match,
        "comp_fit":        comp_fit,
        "remote_fit":      remote_fit,
        "company_quality": company_quality,
        "realism":         realism,
        "composite":       composite,
        "tier":            tier,
        "rationale":       rationale,
    }

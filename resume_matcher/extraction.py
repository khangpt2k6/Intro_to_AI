"""Skill extraction: reduce a noisy document to a structured skill profile.

Each extracted skill carries a mention count and a confidence value. The
confidence is a frequency-based heuristic for now (a skill mentioned three
times is more certain than one mentioned once); replacing it with a Naive
Bayes estimate over section text is on the roadmap.
"""

import re

from .skills import SKILL_ALIASES

# precompile one word-bounded, case-insensitive pattern per canonical skill
_PATTERNS = {
    skill: re.compile(
        r"(?<![\w+#])(" + "|".join(re.escape(a) for a in aliases) + r")(?![\w+#])",
        re.IGNORECASE,
    )
    for skill, aliases in SKILL_ALIASES.items()
}


def extract_skills(text):
    """Return {canonical_skill: {"count": int, "confidence": float}}."""
    profile = {}
    for skill, pattern in _PATTERNS.items():
        count = len(pattern.findall(text))
        if count:
            confidence = min(0.95, 0.60 + 0.10 * count)
            profile[skill] = {"count": count, "confidence": round(confidence, 2)}
    return profile


def parse_job_description(text):
    """Split a job posting into hard and soft constraints (proposal section 2).

    Skills listed under a "Required" heading are hard constraints; skills
    under a "Preferred" / "Nice to have" heading are soft constraints. Skills
    mentioned outside both sections default to soft.
    """
    lower = text.lower()
    req_idx = lower.find("required")
    pref_idx = lower.find("preferred")
    if pref_idx == -1:
        pref_idx = lower.find("nice to have")

    if req_idx != -1 and pref_idx != -1:
        required_text = text[req_idx:pref_idx]
        preferred_text = text[pref_idx:]
    elif req_idx != -1:
        required_text, preferred_text = text[req_idx:], ""
    else:
        required_text, preferred_text = "", text

    hard = set(extract_skills(required_text))
    soft = set(extract_skills(preferred_text)) - hard
    # anything mentioned elsewhere in the posting counts as a soft signal
    soft |= set(extract_skills(text)) - hard - soft
    return {"hard": sorted(hard), "soft": sorted(soft)}

"""Skill extraction: reduce a noisy document to a structured skill profile.

Each extracted skill carries a mention count and a confidence in [0, 1] that
estimates how genuinely the resume demonstrates the skill (vs just listing it).
Confidence blends three signals:

  1. mention frequency  - a skill named three times beats one named once;
  2. experience context - mentions sitting next to action/experience words
     ("built", "developed", "3 years of ...") beat mentions that only appear in
     a flat "Skills:" list;
  3. category agreement - when a Naive Bayes classifier is supplied, a skill
     whose home categories match the resume's predicted category is trusted more
     than a cross-domain hit (see confidence.py).

Without a classifier, extract_skills stays a pure text function (frequency +
context only), so it imports and runs without the dataset or any model.
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

# words that signal a skill was actually used on the job / in a project, rather
# than just parked in a skills list
_ACTION_WORDS = re.compile(
    r"\b(built|build|building|developed|develop|developing|designed|design|"
    r"implemented|implement|created|create|creating|engineered|architected|"
    r"deployed|deploy|delivered|maintained|maintaining|managed|managing|led|"
    r"leading|optimized|automated|launched|integrated|migrated|configured|"
    r"administered|analyzed|conducted|performed|produced|programmed|coded|"
    r"utilized|used|using|leveraged|applied|responsible|experience|years|"
    r"project|projects|worked)\b",
    re.IGNORECASE,
)

_CONTEXT_WINDOW = 60  # chars scanned on each side of a mention for action words

# confidence weights
_W_FREQ_MODEL, _W_CTX_MODEL, _W_AGREE = 0.40, 0.25, 0.35
_W_FREQ_PURE, _W_CTX_PURE = 0.62, 0.38


def _freq_score(count):
    return min(1.0, 0.4 + 0.2 * count)


def _context_score(text, matches):
    """Fraction of mentions that sit near an action/experience word, mapped to
    [0.3, 1.0] so a skills-list-only mention still gets some (but less) credit.
    """
    if not matches:
        return 0.3
    with_context = 0
    for m in matches:
        lo = max(0, m.start() - _CONTEXT_WINDOW)
        window = text[lo:m.end() + _CONTEXT_WINDOW]
        if _ACTION_WORDS.search(window):
            with_context += 1
    return 0.3 + 0.7 * (with_context / len(matches))


def extract_skills(text, classifier=None):
    """Return {canonical_skill: {count, confidence, context, agreement}}.

    Pass a confidence.ConfidenceModel as `classifier` to fold in the NB
    category-agreement signal; omit it for a pure frequency+context estimate.
    """
    text_probs = classifier.category_probs(text) if classifier is not None else None

    profile = {}
    for skill, pattern in _PATTERNS.items():
        matches = list(pattern.finditer(text))
        count = len(matches)
        if not count:
            continue

        freq = _freq_score(count)
        context = _context_score(text, matches)

        if classifier is not None:
            agreement = classifier.agreement(text_probs, skill)
            confidence = (_W_FREQ_MODEL * freq + _W_CTX_MODEL * context
                          + _W_AGREE * agreement)
        else:
            agreement = None
            confidence = _W_FREQ_PURE * freq + _W_CTX_PURE * context

        confidence = max(0.05, min(0.99, confidence))
        profile[skill] = {
            "count": count,
            "confidence": round(confidence, 2),
            "context": round(context, 2),
            "agreement": round(agreement, 2) if agreement is not None else None,
        }
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

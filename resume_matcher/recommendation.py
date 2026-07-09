"""Recommendation engine: greedy best-first ranking of resume edits.

Resume improvement is treated as a search problem (proposal section 2):
a state is a resume, an action is adding or surfacing one missing skill,
and the goal is clearing a target score. Each candidate edit is scored by
the exact coverage points it recovers, and edits are expanded best-first,
largest gain first. Hard constraints dominate because they carry double
the weight of soft ones.
"""

from .matching import HARD_WEIGHT, SOFT_WEIGHT, COVERAGE_WEIGHT


def recommend_edits(match_result, top_k=8):
    """Return missing skills ranked by estimated score gain (points /100)."""
    total_weight = match_result["total_weight"]
    if not total_weight:
        return []

    candidates = []
    for skill in match_result["missing_hard"]:
        gain = 100.0 * COVERAGE_WEIGHT * HARD_WEIGHT / total_weight
        candidates.append({"skill": skill, "kind": "required", "gain": round(gain, 1)})
    for skill in match_result["missing_soft"]:
        gain = 100.0 * COVERAGE_WEIGHT * SOFT_WEIGHT / total_weight
        candidates.append({"skill": skill, "kind": "preferred", "gain": round(gain, 1)})

    candidates.sort(key=lambda c: c["gain"], reverse=True)
    return candidates[:top_k]

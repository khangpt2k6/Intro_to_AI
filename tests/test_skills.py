"""Structural invariants for the skill taxonomy.

These guard the taxonomy as it grows (issue #4 expands it to all 24 dataset
categories): every entry must stay well-formed and aliases must stay
unambiguous, or extraction silently misbehaves.
"""

from resume_matcher.skills import SKILL_ALIASES


def test_taxonomy_is_nonempty_and_well_formed():
    assert isinstance(SKILL_ALIASES, dict) and SKILL_ALIASES
    for canonical, aliases in SKILL_ALIASES.items():
        assert isinstance(canonical, str) and canonical.strip() == canonical
        assert isinstance(aliases, list) and aliases, f"{canonical} has no aliases"
        for alias in aliases:
            assert isinstance(alias, str) and alias
            assert alias == alias.strip(), f"whitespace around alias {alias!r}"
            assert alias == alias.lower(), f"alias {alias!r} must be lowercase"


def test_aliases_unique_within_a_skill():
    for canonical, aliases in SKILL_ALIASES.items():
        assert len(aliases) == len(set(aliases)), f"duplicate alias in {canonical}"


def test_aliases_unambiguous_across_skills():
    """No alias may map to two different canonical skills."""
    seen = {}
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            assert alias not in seen, (
                f"alias {alias!r} maps to both {seen[alias]!r} and {canonical!r}"
            )
            seen[alias] = canonical

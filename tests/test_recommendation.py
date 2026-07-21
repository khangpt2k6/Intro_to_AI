"""Recommendation ranking: required edits outrank preferred, sorted by gain."""

from resume_matcher.recommendation import recommend_edits


def _fake_result():
    return {
        "missing_hard": ["Python", "SQL"],
        "missing_soft": ["Docker"],
        "total_weight": 3.0,
    }


def test_required_edits_outrank_preferred():
    recs = recommend_edits(_fake_result())
    kinds = [r["kind"] for r in recs]
    assert kinds[:2] == ["required", "required"]
    assert kinds[-1] == "preferred"
    # gains are sorted descending
    gains = [r["gain"] for r in recs]
    assert gains == sorted(gains, reverse=True)


def test_top_k_limit():
    assert len(recommend_edits(_fake_result(), top_k=1)) == 1


def test_no_constraints_returns_empty():
    assert recommend_edits({"missing_hard": [], "missing_soft": [],
                            "total_weight": 0}) == []

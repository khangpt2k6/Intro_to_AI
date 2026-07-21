"""Skill extraction behavior: counts, confidence, and word-boundary matching."""

from resume_matcher.extraction import extract_skills, parse_job_description


def test_extract_counts_and_confidence():
    profile = extract_skills("I love Python. Python is great, python python.")
    assert "Python" in profile
    assert profile["Python"]["count"] == 4
    # confidence = min(0.95, 0.60 + 0.10 * count)
    assert profile["Python"]["confidence"] == 0.95


def test_word_boundaries_do_not_over_match():
    # "javascript" must resolve to JavaScript, never the substring "java"
    profile = extract_skills("Experienced in JavaScript development.")
    assert "JavaScript" in profile
    assert "Java" not in profile


def test_absent_skill_not_reported():
    assert extract_skills("just some plain english prose") == {}


def test_parse_job_splits_hard_and_soft():
    job = (
        "Backend Engineer\n"
        "Required:\nPython and SQL are must-haves.\n"
        "Preferred:\nDocker experience is a plus.\n"
    )
    constraints = parse_job_description(job)
    assert "Python" in constraints["hard"]
    assert "SQL" in constraints["hard"]
    assert "Docker" in constraints["soft"]
    # a skill is never both a hard and a soft constraint
    assert not set(constraints["hard"]) & set(constraints["soft"])

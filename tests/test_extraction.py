"""Skill extraction behavior: counts, confidence blend, word-boundary matching."""

from resume_matcher.extraction import extract_skills, parse_job_description


def test_counts_are_exact():
    profile = extract_skills("I love Python. Python is great, python python.")
    assert profile["Python"]["count"] == 4


def test_confidence_in_unit_range_and_rises_with_context():
    listed = extract_skills("Skills: Python")
    demonstrated = extract_skills(
        "Built and deployed Python services; developed Python tooling.")
    assert 0.0 < listed["Python"]["confidence"] <= 0.99
    # experience/action context beats a bare skills-list mention
    assert demonstrated["Python"]["confidence"] > listed["Python"]["confidence"]
    # without a classifier the NB agreement signal is not computed
    assert listed["Python"]["agreement"] is None


def test_confidence_rises_with_frequency():
    one = extract_skills("Python")["Python"]["confidence"]
    many = extract_skills("Python python Python python python")["Python"]["confidence"]
    assert many >= one


def test_word_boundaries_do_not_over_match():
    profile = extract_skills("Experienced in JavaScript development.")
    assert "JavaScript" in profile
    assert "Java" not in profile


def test_absent_skill_not_reported():
    assert extract_skills("just some plain everyday writing here") == {}


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
    assert not set(constraints["hard"]) & set(constraints["soft"])

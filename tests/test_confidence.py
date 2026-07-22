"""Naive Bayes skill-confidence model.

Uses a tiny synthetic two-domain corpus so the test needs neither the 113MB
dataset nor torch.
"""

from resume_matcher.confidence import ConfidenceModel
from resume_matcher.extraction import extract_skills

TECH = [
    "python java sql backend software engineer rest api microservices",
    "python developer machine learning data pipeline docker kubernetes",
    "software engineering git aws rest api backend services",
]
FINANCE = [
    "accounting general ledger tax audit gaap financial statements",
    "accounts payable payroll quickbooks cpa budgeting reconciliation",
    "financial reporting internal audit taxation accountant",
]
CORPUS = TECH + FINANCE
CATS = (["INFORMATION-TECHNOLOGY"] * len(TECH)
        + ["ACCOUNTANT"] * len(FINANCE))


def _model():
    return ConfidenceModel(CORPUS, CATS)


def test_category_probs_form_a_distribution():
    probs = _model().category_probs("python backend api developer")
    assert abs(sum(probs) - 1.0) < 1e-6
    assert all(0.0 <= p <= 1.0 for p in probs)


def test_agreement_is_higher_on_matching_domain():
    model = _model()
    tech_probs = model.category_probs("python java backend rest api developer")
    fin_probs = model.category_probs("tax audit gaap general ledger accountant")
    # "Python" should be trusted more on a tech-reading resume than a finance one
    assert model.agreement(tech_probs, "Python") > model.agreement(fin_probs, "Python")


def test_extract_with_classifier_adds_agreement():
    model = _model()
    profile = extract_skills("Built a python backend and rest api services", model)
    assert profile["Python"]["agreement"] is not None
    assert 0.0 <= profile["Python"]["agreement"] <= 1.0
    assert 0.0 < profile["Python"]["confidence"] <= 0.99

"""Naive Bayes skill-confidence signal.

Binary alias matching (extraction.py) tells us a skill is *mentioned*; it can't
tell us whether the resume genuinely demonstrates it or just name-drops it. This
module adds the category-agreement signal the proposal promised: a small
Multinomial Naive Bayes classifier estimates P(category | resume_text) for the
24 dataset categories, and each skill gets an expected category profile derived
from the same model. A skill whose home categories match the resume's predicted
category (e.g. "TensorFlow" on a resume that reads as INFORMATION-TECHNOLOGY) is
trusted more than a cross-domain hit (the same "TensorFlow" on an ACCOUNTANT
resume).

The model is a plain TF-IDF + MultinomialNB pipeline - the same setup evaluated
in run_experiments.py - used here purely as a probability estimator. It needs no
torch, so extraction/matching stay importable without the deep-learning stack.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from .skills import SKILL_ALIASES


def _cosine(a, b):
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


class ConfidenceModel:
    """P(category | text) plus a per-skill category profile, from one NB model."""

    def __init__(self, corpus_texts, corpus_categories):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(stop_words="english", max_features=20000,
                                      ngram_range=(1, 2), sublinear_tf=True)),
            ("clf", MultinomialNB(alpha=0.1)),
        ])
        self.pipeline.fit(list(corpus_texts), list(corpus_categories))
        self.classes_ = self.pipeline.classes_

        # Each skill's expected category profile = the model's P(category | ...)
        # for a pseudo-document made of the skill's alias phrases. Cheap: one
        # predict_proba call over the ~240 skills, no corpus re-scan.
        skills = list(SKILL_ALIASES)
        pseudo_docs = [" ".join(SKILL_ALIASES[s]) for s in skills]
        profiles = self.pipeline.predict_proba(pseudo_docs)
        self._skill_profile = {s: profiles[i] for i, s in enumerate(skills)}

    def category_probs(self, text):
        """Return P(category | text) as a vector aligned with self.classes_."""
        return self.pipeline.predict_proba([text])[0]

    def agreement(self, text_probs, skill):
        """Cosine between the resume's category distribution and the skill's.

        ~1.0 when the resume reads as the skill's home domain, ~0 when it reads
        as an unrelated domain. Skills the model has no signal for get a diffuse
        profile, which lands at a neutral middling value rather than a penalty.
        """
        profile = self._skill_profile.get(skill)
        if profile is None:
            return 0.5
        return _cosine(text_probs, profile)

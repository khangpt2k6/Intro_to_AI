"""Matching engine: TF-IDF vector space model + constraint-style skill coverage
+ pre-trained Sentence-BERT semantic similarity.

The final compatibility score combines three signals:

1. Skill coverage (weight 0.4): fraction of the job's constraints satisfied,
   with hard (required) constraints weighted 1.0 and soft (preferred)
   constraints weighted 0.5.
2. Corpus percentile (weight 0.3): where this resume's TF-IDF cosine
   similarity to the job description ranks against every resume in the
   2,484-document corpus. Percentile calibration keeps the raw cosine
   values (which are small in absolute terms) interpretable.
3. Semantic similarity (weight 0.3): cosine similarity between
   pre-trained Sentence-BERT embeddings of the resume and job text, which
   catches paraphrased/lexically-different but semantically equivalent
   phrasing that TF-IDF misses.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .extraction import extract_skills, parse_job_description
from .semantic import semantic_similarity

HARD_WEIGHT = 1.0
SOFT_WEIGHT = 0.5
COVERAGE_WEIGHT = 0.4
SIMILARITY_WEIGHT = 0.3
SBERT_WEIGHT = 0.3


class ResumeMatcher:
    def __init__(self, corpus_texts, classifier=None):
        # optional confidence.ConfidenceModel; when present, extracted skills
        # carry an NB category-agreement signal and coverage is confidence-weighted
        self.classifier = classifier
        self.vectorizer = TfidfVectorizer(
            stop_words="english", max_features=20000, ngram_range=(1, 2),
            sublinear_tf=True,
        )
        self.corpus_matrix = self.vectorizer.fit_transform(corpus_texts)

    def match(self, resume_text, job_text):
        resume_vec = self.vectorizer.transform([resume_text])
        job_vec = self.vectorizer.transform([job_text])

        cosine = float(cosine_similarity(resume_vec, job_vec)[0, 0])
        corpus_cosines = cosine_similarity(self.corpus_matrix, job_vec).ravel()
        percentile = float((corpus_cosines < cosine).mean())

        sbert_cos = semantic_similarity(resume_text, job_text)

        constraints = parse_job_description(job_text)
        resume_skills = extract_skills(resume_text, self.classifier)

        def _conf(skill):
            return resume_skills[skill]["confidence"]

        matched_hard = [s for s in constraints["hard"] if s in resume_skills]
        missing_hard = [s for s in constraints["hard"] if s not in resume_skills]
        matched_soft = [s for s in constraints["soft"] if s in resume_skills]
        missing_soft = [s for s in constraints["soft"] if s not in resume_skills]

        # each matched constraint is credited by the resume's confidence in that
        # skill, so a genuinely-demonstrated skill counts more than a name-dropped
        # one. The denominator stays count-based so coverage stays in [0, 1].
        total_weight = (HARD_WEIGHT * len(constraints["hard"])
                        + SOFT_WEIGHT * len(constraints["soft"]))
        earned_weight = (HARD_WEIGHT * sum(_conf(s) for s in matched_hard)
                         + SOFT_WEIGHT * sum(_conf(s) for s in matched_soft))
        coverage = earned_weight / total_weight if total_weight else 0.0

        score = 100.0 * (COVERAGE_WEIGHT * coverage
                         + SIMILARITY_WEIGHT * percentile
                         + SBERT_WEIGHT * sbert_cos)

        return {
            "score": round(score, 1),
            "coverage": round(coverage, 3),
            "cosine": round(cosine, 4),
            "percentile": round(percentile, 3),
            "sbert_cos": round(sbert_cos, 4),
            "matched_hard": matched_hard,
            "missing_hard": missing_hard,
            "matched_soft": matched_soft,
            "missing_soft": missing_soft,
            "confidence": {s: _conf(s) for s in matched_hard + matched_soft},
            "resume_skills": resume_skills,
            "total_weight": total_weight,
        }

"""Semantic similarity via a pre-trained Sentence-BERT model.

Used strictly as a black-box embedder: the model is downloaded pre-trained
and never fine-tuned. Any report text describing this component should say
"pre-trained Sentence-BERT used for sentence embeddings," not that a model
was trained.
"""

from sentence_transformers import SentenceTransformer, util

_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def semantic_similarity(resume_text, job_text):
    model = _get_model()
    embeddings = model.encode([resume_text, job_text], convert_to_tensor=True)
    return float(util.cos_sim(embeddings[0], embeddings[1]).item())

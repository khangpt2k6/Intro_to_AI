# Resume Analyzer and Job Matcher

CAI4002 Introduction to Artificial Intelligence - group project.

An AI application that measures how well a resume fits a specific job
description: it extracts skills from both documents with NLP, computes a
compatibility score (TF-IDF vector space model + constraint-style skill
coverage + pre-trained Sentence-BERT semantic similarity), classifies the
resume into a job category with a Naive Bayes model, and recommends the edits
that raise the score the most.

**Team:** Martin Dang, Tuan Khang Phan

## Project layout

```
resume_matcher/        core package
  skills.py            canonical skill taxonomy with aliases (24 categories)
  extraction.py        skill extraction + confidence + job constraint parsing
  confidence.py        Naive Bayes category-agreement signal for confidence
  matching.py          TF-IDF cosine + weighted skill coverage + SBERT score
  semantic.py          pre-trained Sentence-BERT sentence-embedding similarity
  ingest.py            load resume text from .pdf / .docx / .txt
  recommendation.py    greedy best-first ranking of resume edits
sample_jobs/           example job postings used in the demo
sample_resumes/        example resume files (pdf/docx) for the upload path
run_experiments.py     trains and evaluates the category classifiers, saves figures
demo.py                end-to-end demo: one resume vs three job postings
```

## Setup

```
pip install -r requirements.txt
python -c "import kagglehub; print(kagglehub.dataset_download('snehaanbhawal/resume-dataset'))"
```

Copy `Resume/Resume.csv` from the downloaded dataset into `data/resume-dataset/Resume.csv`
(the `data/` folder is gitignored because of its size).

Dataset: [Resume Dataset (Kaggle)](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset) -
2,484 real resumes labeled into 24 job categories.

## Run

```
python run_experiments.py                 # classifier metrics + report figures
python demo.py                            # match one IT resume against three job postings
python demo.py --resume path/to/cv.pdf    # match an uploaded pdf/docx/txt resume
streamlit run app.py                      # interactive web UI
pytest -q                                 # unit tests
```

## Web UI

`streamlit run app.py` opens a browser app: upload (or paste) a resume, pick or
paste a job description, and see the compatibility score with its component
breakdown, matched vs missing skills, the Naive Bayes predicted job category,
and the top recommended edits. The corpus, matcher, and models load once and are
cached (`@st.cache_resource`).

## Skill confidence

`extract_skills()` reports, for every skill it finds, a confidence in [0, 1]
estimating how genuinely the resume demonstrates that skill rather than just
listing it. Confidence is a weighted blend of three signals:

- **Mention frequency** - a skill named several times scores higher than one
  named once.
- **Experience context** - a mention sitting next to action/experience words
  ("built", "developed", "3 years of ...") scores higher than one that only
  appears in a flat "Skills:" list.
- **Category agreement (Naive Bayes)** - a Multinomial NB classifier estimates
  P(category | resume) over the 24 categories. Each skill has an expected
  category profile from the same model, and agreement is the cosine between the
  two distributions. A skill whose home domain matches the resume's predicted
  category (TensorFlow on an IT resume) is trusted more than a cross-domain hit
  (the same TensorFlow on an accountant resume).

With a classifier the weights are 0.40 / 0.25 / 0.35 (frequency / context /
agreement); without one, confidence uses frequency and context only, so
`extract_skills()` still runs as a pure text function with no model or dataset.
The matcher credits each matched job requirement by the resume's confidence in
that skill, so a genuinely-demonstrated skill contributes more to the coverage
score than a name-dropped one.

## How the compatibility score works

The final 0-100 score is a weighted sum of three components:

- **Skill coverage (0.4)** - confidence-weighted fraction of the job's
  constraints the resume satisfies (required skills weighted 1.0, preferred 0.5).
- **Corpus percentile (0.3)** - where the resume's TF-IDF cosine similarity to
  the job ranks against all 2,484 resumes.
- **Semantic similarity (0.3)** - cosine between pre-trained Sentence-BERT
  embeddings of the resume and the job text (used strictly as a black-box
  embedder, never fine-tuned).

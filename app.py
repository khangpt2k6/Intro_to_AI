"""Minimal Streamlit web UI for the resume/job matcher.

Run with:  streamlit run app.py

Upload (or paste) a resume, pick or paste a job description, and see the overall
compatibility score, its component breakdown, matched vs missing skills, the
predicted job category, and the top recommended resume edits.
"""

import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from resume_matcher.confidence import ConfidenceModel
from resume_matcher.ingest import load_resume
from resume_matcher.matching import ResumeMatcher
from resume_matcher.recommendation import recommend_edits

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "resume-dataset" / "Resume.csv"
JOBS = ROOT / "sample_jobs"

st.set_page_config(page_title="Resume Analyzer and Job Matcher",
                   page_icon="🧭", layout="wide")


@st.cache_resource(show_spinner="Loading corpus, training NB model, building matcher...")
def load_engine():
    """Load the corpus and build the matcher + confidence model once per session."""
    df = pd.read_csv(DATA)
    corpus = df["Resume_str"].tolist()
    classifier = ConfidenceModel(corpus, df["Category"])
    matcher = ResumeMatcher(corpus, classifier=classifier)
    return matcher, classifier


@st.cache_data(show_spinner=False)
def sample_jobs():
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(JOBS.glob("*.txt"))}


def read_uploaded(uploaded):
    """Persist an uploaded file to a temp path and run it through ingest.load_resume."""
    suffix = Path(uploaded.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        tmp_path = tmp.name
    return load_resume(tmp_path)


st.title("Resume Analyzer and Job Matcher")
st.caption("CAI4002 - TF-IDF + skill coverage + Sentence-BERT, with Naive Bayes "
           "skill confidence")

if not DATA.exists():
    st.error(
        f"Dataset not found at `{DATA}`. Download it and copy `Resume.csv` there:\n\n"
        "```\n"
        "pip install -r requirements.txt\n"
        "python -c \"import kagglehub; print(kagglehub.dataset_download('snehaanbhawal/resume-dataset'))\"\n"
        "```"
    )
    st.stop()

jobs = sample_jobs()

left, right = st.columns(2)

with left:
    st.subheader("Resume")
    uploaded = st.file_uploader("Upload a resume (.pdf, .docx, .txt)",
                                type=["pdf", "docx", "txt"])
    resume_text = st.text_area(
        "...or paste the resume text",
        height=280,
        placeholder="Paste resume text here if you are not uploading a file.",
    )

with right:
    st.subheader("Job description")
    choice = st.selectbox("Prefill a sample posting",
                          ["(none)"] + list(jobs.keys()))
    prefill = jobs.get(choice, "")
    job_text = st.text_area("Job description", value=prefill, height=280,
                            placeholder="Paste a job description or pick a sample above.")

analyze = st.button("Analyze match", type="primary")

if analyze:
    # resolve the resume text: uploaded file takes precedence over pasted text
    if uploaded is not None:
        try:
            resume_text = read_uploaded(uploaded)
        except Exception as exc:  # noqa: BLE001 - surface any ingest error to the user
            st.error(f"Could not read the uploaded file: {exc}")
            st.stop()

    if not resume_text.strip():
        st.warning("Please upload or paste a resume.")
        st.stop()
    if not job_text.strip():
        st.warning("Please paste or pick a job description.")
        st.stop()

    matcher, classifier = load_engine()
    result = matcher.match(resume_text, job_text)
    recs = recommend_edits(result, top_k=8)
    predicted = classifier.top_categories(resume_text, k=3)

    st.divider()
    top = st.columns([1.2, 1, 1, 1])
    top[0].metric("Compatibility score", f"{result['score']}/100")
    top[1].metric("Skill coverage", f"{result['coverage']:.0%}")
    top[2].metric("Corpus percentile", f"{result['percentile']:.0%}")
    top[3].metric("Semantic (SBERT)", f"{result['sbert_cos']:.2f}")

    st.caption(
        f"Score = 0.4 x coverage + 0.3 x percentile + 0.3 x SBERT. "
        f"TF-IDF cosine to this job = {result['cosine']:.3f}."
    )

    pred_str = ", ".join(f"{cat} ({p:.0%})" for cat, p in predicted)
    st.info(f"**Predicted resume category (Naive Bayes):** {pred_str}")

    conf = result["confidence"]
    m_left, m_right = st.columns(2)
    with m_left:
        st.markdown("### Matched skills")
        matched = result["matched_hard"] + result["matched_soft"]
        if matched:
            for s in result["matched_hard"]:
                st.markdown(f"- **{s}** (required) - confidence {conf[s]:.2f}")
            for s in result["matched_soft"]:
                st.markdown(f"- {s} (preferred) - confidence {conf[s]:.2f}")
        else:
            st.markdown("_none_")
    with m_right:
        st.markdown("### Missing skills")
        if result["missing_hard"] or result["missing_soft"]:
            for s in result["missing_hard"]:
                st.markdown(f"- **{s}** (required)")
            for s in result["missing_soft"]:
                st.markdown(f"- {s} (preferred)")
        else:
            st.markdown("_none_")

    st.markdown("### Top recommended edits")
    if recs:
        st.table(pd.DataFrame(
            [{"skill": r["skill"], "kind": r["kind"],
              "estimated gain (pts)": r["gain"]} for r in recs]
        ))
    else:
        st.markdown("_no missing constraints - this resume already covers the job._")

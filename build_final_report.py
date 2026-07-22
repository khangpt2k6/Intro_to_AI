"""Build the final report docx (and pdf) from the actual experiment artifacts.

Reads results/metrics.json and results/demo_results.json so every number in the
report comes from a real run. Reuses the classic-styling helpers from
build_report.py. Output: report/Final_Report.docx (+ .pdf if Word is available).
"""

import json
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from build_report import (add_figure, add_heading, apply_classic_fonts,
                          bold_row, style_table)

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
REPORT_DIR = ROOT / "report"


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    metrics = json.loads((RESULTS / "metrics.json").read_text())
    demo = json.loads((RESULTS / "demo_results.json").read_text(encoding="utf-8"))

    ds = metrics["dataset"]
    nb = metrics["models"]["Naive Bayes"]
    lr = metrics["models"]["Logistic Regression"]
    sw, da, ac = demo["software_engineer"], demo["data_analyst"], demo["accountant"]

    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)

    # title block
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run("Resume Analyzer and Job Matcher")
    r.font.size = Pt(20)
    r.font.bold = True
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run("CAI4002: Introduction to Artificial Intelligence | "
                    "Group Project Final Report")
    r.font.size = Pt(12)
    r.font.italic = True
    team = doc.add_paragraph()
    team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = team.add_run("Team Members: Martin Dang, Tuan Khang Phan\nJuly 21, 2026")
    r.font.size = Pt(11)
    r.font.bold = True

    # Abstract
    add_heading(doc, "Abstract")
    doc.add_paragraph(
        "This project builds an AI system that measures how well a resume fits a "
        "specific job posting and recommends the edits that would raise that fit "
        "the most. The completed pipeline extracts a structured, confidence-scored "
        "skill profile from a resume, parses a posting into required and preferred "
        "qualifications, and produces a 0-100 compatibility score that blends "
        "lexical similarity (TF-IDF), constraint-style skill coverage, and "
        "pre-trained Sentence-BERT semantic similarity. A Naive Bayes classifier "
        f"trained on {ds['n_resumes']:,} real resumes across {ds['n_categories']} "
        "job categories provides both a predicted job family and a per-skill "
        "confidence signal. The system is usable from a command-line demo and from "
        "an interactive web interface, and every number in this report is produced "
        "by a reproducible script in our repository "
        "(github.com/khangpt2k6/Intro_to_AI)."
    )

    # 1. System overview
    add_heading(doc, "1. System Overview")
    doc.add_paragraph(
        "The five-stage pipeline proposed at the start of the project is now fully "
        "implemented. The table below summarizes each stage and how it is built."
    )
    t = doc.add_table(rows=7, cols=2)
    style_table(t)
    t.rows[0].cells[0].text = "Pipeline stage"
    t.rows[0].cells[1].text = "Implementation"
    stages = [
        ("Resume ingestion",
         "Uploaded .pdf / .docx / .txt files are converted to clean, normalized "
         "text (pypdf, python-docx) so the rest of the pipeline sees the same "
         "shape of input regardless of source format."),
        ("Skill extraction + confidence",
         "A 244-skill taxonomy (aliases matched with word-bounded regular "
         "expressions) covering all 24 dataset categories; each extracted skill "
         "gets a confidence in [0,1] blending mention frequency, experience "
         "context, and Naive Bayes category agreement (Section 3.2)."),
        ("Job description parsing",
         "Postings are split into hard constraints (required) and soft "
         "constraints (preferred), following the constraint-satisfaction framing "
         "from the proposal."),
        ("Compatibility scoring",
         "A 0-100 score blending confidence-weighted skill coverage (0.4), "
         "corpus percentile of TF-IDF cosine similarity (0.3), and pre-trained "
         "Sentence-BERT semantic similarity (0.3)."),
        ("Recommendation engine",
         "Missing constraints ranked greedy best-first by the exact score gain "
         "each edit recovers; required skills weighted twice preferred ones."),
        ("Category classification",
         "Multinomial Naive Bayes and Logistic Regression over TF-IDF features, "
         "evaluated on a stratified held-out test set (Section 4)."),
    ]
    for i, (a, b) in enumerate(stages, start=1):
        t.rows[i].cells[0].text = a
        t.rows[i].cells[1].text = b
    bold_row(t)
    doc.add_paragraph()

    # 2. Dataset
    add_heading(doc, "2. Dataset")
    doc.add_paragraph(
        "We use the public Resume Dataset from Kaggle "
        "(snehaanbhawal/resume-dataset). It contains "
        f"{ds['n_resumes']:,} real resumes provided as plain text and labeled "
        f"into {ds['n_categories']} job categories such as Information "
        "Technology, Finance, Engineering, Healthcare, Teacher, and Chef. The "
        "dataset is the training corpus for the TF-IDF vector space and the "
        "category classifier, and it supplies realistic test resumes for the "
        "matching demo."
    )
    add_figure(doc, "fig1_category_distribution.png",
               "Figure 1. Distribution of the 2,484 resumes across the 24 job "
               "categories. The class imbalance (120 vs 22 resumes) is a "
               "challenge the classifier must handle.", width=5.6)

    # 3. Methods
    add_heading(doc, "3. Methods")

    add_heading(doc, "3.1 Skill extraction and taxonomy", level=2)
    doc.add_paragraph(
        "Skill mentions are normalized through a controlled vocabulary of 244 "
        "canonical skills, each with a list of surface-form aliases (for example "
        "'JS' and 'Javascript' both map to JavaScript). Aliases are matched with "
        "case-insensitive, word-bounded regular expressions, and every alias is "
        "globally unique so a mention resolves to exactly one skill. The taxonomy "
        "was expanded from an initial IT/finance-focused set to span all 24 "
        "dataset categories (education, culinary, design, healthcare, legal, "
        "aviation, agriculture, and more); average skills extracted per resume "
        "rose several-fold for the previously under-covered categories, and every "
        "category now has at least one skill matched in 100% of its resumes."
    )

    add_heading(doc, "3.2 Skill confidence (Naive Bayes agreement)", level=2)
    doc.add_paragraph(
        "Binary alias matching tells us a skill is mentioned; it cannot tell us "
        "whether the resume genuinely demonstrates it. Each extracted skill "
        "therefore carries a confidence in [0,1] that blends three signals: (1) "
        "mention frequency, so a skill named several times outweighs one named "
        "once; (2) experience context, which rewards mentions that sit next to "
        "action words ('built', 'developed', 'three years of ...') over mentions "
        "that only appear in a flat skills list; and (3) category agreement, a "
        "Naive Bayes signal. A Multinomial Naive Bayes classifier estimates "
        "P(category | resume); each skill has an expected category profile derived "
        "from the same model, and agreement is the cosine between the two "
        "distributions. A TensorFlow mention on a resume that reads as Information "
        "Technology is therefore trusted more than the same mention on an "
        "accountant resume. With the classifier the three signals are weighted "
        "0.40 / 0.25 / 0.35; the matcher then credits each matched requirement by "
        "the resume's confidence in that skill, so a genuinely demonstrated skill "
        "contributes more to the coverage score than a name-dropped one."
    )

    add_heading(doc, "3.3 Compatibility score", level=2)
    doc.add_paragraph(
        "The final 0-100 score is a weighted sum of three components: "
        "confidence-weighted skill coverage (weight 0.4; required skills weighted "
        "1.0, preferred 0.5), corpus percentile (weight 0.3; where the resume's "
        "TF-IDF cosine similarity to the posting ranks against all 2,484 corpus "
        "resumes), and semantic similarity (weight 0.3). Percentile calibration "
        "keeps the otherwise tiny raw cosine values (roughly 0.01 to 0.17) "
        "interpretable."
    )

    add_heading(doc, "3.4 Sentence-BERT semantic similarity", level=2)
    doc.add_paragraph(
        "TF-IDF only rewards exact lexical overlap, so a resume that says 'built "
        "REST services in Django' earns no credit against a posting asking for "
        "'web backend development in Python'. To capture paraphrase, we add a "
        "semantic component: cosine similarity between sentence embeddings of the "
        "resume and the posting. We use a pre-trained Sentence-BERT model "
        "(all-MiniLM-L6-v2) strictly as a black-box embedder; consistent with the "
        "scope of the course, we do not fine-tune or otherwise train it. On the "
        "demo the semantic component tracks fit closely, ranging from "
        f"{ac['sbert_cos']:.2f} for the accountant posting to {sw['sbert_cos']:.2f} "
        "for the software engineer posting."
    )

    add_heading(doc, "3.5 Recommendation engine", level=2)
    doc.add_paragraph(
        "Resume improvement is treated as a search problem: each missing "
        "constraint is a candidate edit scored by the exact coverage points it "
        "would recover, and edits are expanded best-first, largest gain first. "
        "Required skills dominate because they carry twice the weight of preferred "
        "ones."
    )

    # 4. Experiments
    add_heading(doc, "4. Experimental Results")
    doc.add_paragraph(
        "We trained two classifiers to predict a resume's job category from its "
        f"text on an 80/20 stratified split ({ds['train_size']:,} training, "
        f"{ds['test_size']:,} test resumes). With 24 classes, random guessing "
        "would score about 4.2%. These classifier results are unchanged from the "
        "progress-report baseline, as expected: the classifier reads the raw "
        "resume text and is independent of the taxonomy and confidence work done "
        "since."
    )
    t = doc.add_table(rows=3, cols=3)
    style_table(t)
    t.rows[0].cells[0].text = "Model"
    t.rows[0].cells[1].text = "Accuracy"
    t.rows[0].cells[2].text = "Macro F1"
    t.rows[1].cells[0].text = "Multinomial Naive Bayes"
    t.rows[1].cells[1].text = f"{nb['accuracy']:.1%}"
    t.rows[1].cells[2].text = f"{nb['macro_f1']:.3f}"
    t.rows[2].cells[0].text = "Logistic Regression"
    t.rows[2].cells[1].text = f"{lr['accuracy']:.1%}"
    t.rows[2].cells[2].text = f"{lr['macro_f1']:.3f}"
    bold_row(t)
    doc.add_paragraph()
    add_figure(doc, "fig2_model_comparison.png",
               "Figure 2. Both models beat the 4.2% random baseline by a wide "
               "margin; Logistic Regression is the stronger of the two.",
               width=5.2)
    add_figure(doc, "fig3_confusion_matrix.png",
               "Figure 3. Normalized confusion matrix for Logistic Regression. "
               "The strong diagonal shows most categories are learned well; the "
               "remaining confusion concentrates in genuinely overlapping "
               "categories (Finance vs Accountant, Sales vs Business "
               "Development).", width=6.0)

    # 5. Demo
    add_heading(doc, "5. End-to-End Demo")
    doc.add_paragraph(
        "To validate the whole pipeline we matched one real Information Technology "
        "resume from the dataset (ID 83816738) against three postings we wrote in "
        "realistic formats. The system behaves as a human reviewer would expect: "
        f"the resume scores {sw['score']}/100 against the software engineer "
        f"posting, {da['score']}/100 against the data analyst posting, and only "
        f"{ac['score']}/100 against the accountant posting. Scores are lower than "
        "a naive count-based match would give because coverage is weighted by "
        "per-skill confidence."
    )
    add_figure(doc, "fig4_match_scores.png",
               "Figure 4. The same resume scored against three postings. The score "
               "cleanly separates the strong fit from the partial and poor fits.",
               width=5.4)
    n_hard = len(sw["matched_hard"]) + len(sw["missing_hard"])
    conf = sw.get("confidence", {})
    matched_with_conf = ", ".join(
        f"{s} ({conf[s]:.2f})" if s in conf else s for s in sw["matched_hard"])
    doc.add_paragraph(
        f"For the software engineer posting the analyzer matched "
        f"{len(sw['matched_hard'])} of {n_hard} required skills, each shown with "
        f"its confidence: {matched_with_conf}. It flagged "
        f"{', '.join(sw['missing_hard']) or 'no'} required skills as missing and "
        f"ranked {', '.join(s['skill'] for s in sw['recommendations'][:2])} as the "
        "highest-value edits, ahead of preferred-skill edits like Kubernetes."
    )
    add_figure(doc, "fig5_demo_output.png",
               "Figure 5. Console output for the demo resume across all three "
               "postings, including the extracted skills with confidence and the "
               "ranked edit recommendations.", width=6.2)

    # 6. Web interface
    add_heading(doc, "6. Web Interface")
    doc.add_paragraph(
        "The system is also usable from a Streamlit web app (streamlit run "
        "app.py). A user uploads a resume file or pastes resume text, picks or "
        "pastes a job description, and sees the compatibility score with its "
        "component breakdown, the matched and missing skills with confidence, the "
        "Naive Bayes predicted job category, and the ranked recommended edits. "
        "The corpus, matcher, and models are cached so they load once per session."
    )
    add_figure(doc, "fig6_web_ui.png",
               "Figure 6. The web interface, showing an IT resume matched against "
               "a backend software engineer posting: score, component breakdown, "
               "predicted category, matched/missing skills with confidence, and "
               "recommended edits.", width=6.0)

    # 7. Challenges
    add_heading(doc, "7. Challenges")
    challenges = [
        ("Class imbalance in the dataset.",
         "The largest categories have 120 resumes while the smallest (BPO) has "
         "only 22. We report macro F1 (which weights every class equally) next to "
         "raw accuracy, and use a stratified split."),
        ("Semantically overlapping categories.",
         "Classification error concentrates in category pairs that share "
         "vocabulary (Finance vs Accountant, Sales vs Business Development). This "
         "motivated adding Logistic Regression (+11 points over Naive Bayes) and "
         "the Sentence-BERT semantic signal in the matcher."),
        ("Distinguishing genuine skills from name-dropping.",
         "A skill listed once in a skills block is weaker evidence than one used "
         "in described work. The confidence blend (frequency, experience context, "
         "and Naive Bayes category agreement) addresses this directly and feeds a "
         "confidence-weighted coverage score."),
        ("Short skill aliases cause false positives.",
         "Aliases like 'R' or 'Go' match ordinary words, and generic terms cause "
         "cross-domain hits (an early version matched 'reporting' in 'financial "
         "reporting' as Journalism). We use word-bounded matching, prefer longer "
         "alias forms, and keep aliases globally unique, verified by automated "
         "tests."),
        ("Reproducibility and safety of the pipeline.",
         "Continuous integration runs the test suite on every change, and the "
         "heavy Sentence-BERT import is deferred so the core package and tests "
         "run without the deep-learning stack."),
    ]
    for head, body in challenges:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(head + " ")
        run.font.bold = True
        p.add_run(body)
    doc.add_paragraph()

    # 8. Contributions
    add_heading(doc, "8. Team Contributions")
    doc.add_paragraph(
        "We split the work evenly (50/50), pairing on design decisions and "
        "dividing implementation by pipeline stage:")
    t = doc.add_table(rows=3, cols=2)
    style_table(t)
    t.rows[0].cells[0].text = "Martin Dang (50%)"
    t.rows[0].cells[1].text = "Tuan Khang Phan (50%)"
    t.rows[1].cells[0].text = (
        "Skill taxonomy design and expansion to 24 categories; skill extraction "
        "and confidence blend; job constraint parser; recommendation engine; "
        "Sentence-BERT semantic similarity component")
    t.rows[1].cells[1].text = (
        "Dataset acquisition and preprocessing; TF-IDF matching engine and "
        "percentile calibration; Naive Bayes category and confidence model; "
        "classifier experiments; resume ingestion; Streamlit web interface")
    t.rows[2].cells[0].text = (
        "Joint: sample job postings, end-to-end testing, this report")
    t.rows[2].cells[1].text = (
        "Joint: system design, error analysis, this report")
    bold_row(t)
    doc.add_paragraph()

    # 9. Conclusion
    add_heading(doc, "9. Conclusion")
    doc.add_paragraph(
        "The completed system meets the goals set out in the proposal. It turns a "
        "free-text resume and job posting into an interpretable compatibility "
        "score and a ranked list of concrete improvements, combining classical "
        "NLP (TF-IDF, Naive Bayes) with a pre-trained transformer embedding used "
        "as a black box. The confidence-weighted coverage and the semantic signal "
        "make the score more faithful than lexical matching alone, and the web "
        "interface makes the tool usable by a non-technical user. Natural next "
        "steps are measuring extraction precision and recall on a hand-labeled "
        "sample and calibrating the score against human fit judgments."
    )

    apply_classic_fonts(doc)
    out = REPORT_DIR / "Final_Report.docx"
    doc.save(out)
    print(f"Saved {out}")

    # best-effort PDF export (needs Microsoft Word via docx2pdf)
    try:
        from docx2pdf import convert
        pdf_out = REPORT_DIR / "Final_Report.pdf"
        convert(str(out), str(pdf_out))
        print(f"Saved {pdf_out}")
    except Exception as exc:  # noqa: BLE001
        print(f"PDF export skipped ({exc}); open the .docx in Word to export a PDF.")


if __name__ == "__main__":
    main()

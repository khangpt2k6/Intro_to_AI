"""End-to-end demo: match one real resume from the dataset against three
sample job postings, print the analysis, and save the artifacts the report
uses (match scores, recommendations, a rendered output image).

Outputs:
  results/demo_results.json
  results/demo_output.txt
  figures/fig4_match_scores.png
  figures/fig5_demo_output.png
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from resume_matcher.matching import ResumeMatcher
from resume_matcher.recommendation import recommend_edits

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "resume-dataset" / "Resume.csv"
JOBS = ROOT / "sample_jobs"
FIGURES = ROOT / "figures"
RESULTS = ROOT / "results"

BLUE = "#2a78d6"
INK = "#0b0b0b"
MUTED = "#898781"
SURFACE = "#fcfcfb"


def render_text_figure(text, path):
    """Render console output as an image (the report's 'screenshot')."""
    lines = text.splitlines()
    fig, ax = plt.subplots(figsize=(8.6, 0.165 * len(lines) + 0.6))
    ax.axis("off")
    fig.patch.set_facecolor("#1a1a19")
    ax.text(0.01, 0.99, text, family="Consolas", fontsize=7.6,
            va="top", ha="left", color="#e8e8e3", transform=ax.transAxes)
    fig.savefig(path, dpi=200, bbox_inches="tight",
                facecolor="#1a1a19", pad_inches=0.25)
    plt.close(fig)


def main():
    FIGURES.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)

    df = pd.read_csv(DATA)
    corpus = df["Resume_str"].tolist()

    # a fixed, reproducible test subject: the first IT resume in the dataset
    it_rows = df[df["Category"] == "INFORMATION-TECHNOLOGY"]
    resume_row = it_rows.iloc[0]
    resume_text = resume_row["Resume_str"]

    print("Building TF-IDF matcher over the 2,484-resume corpus...")
    matcher = ResumeMatcher(corpus)

    lines = []
    lines.append("RESUME ANALYZER AND JOB MATCHER - DEMO")
    lines.append(f"Test resume: dataset ID {resume_row['ID']} "
                 f"(true category: {resume_row['Category']})")
    lines.append("=" * 74)

    all_results = {}
    for job_file in sorted(JOBS.glob("*.txt")):
        job_text = job_file.read_text(encoding="utf-8")
        job_title = job_text.splitlines()[0].strip()
        result = matcher.match(resume_text, job_text)
        recs = recommend_edits(result, top_k=5)
        all_results[job_file.stem] = {"title": job_title, **result,
                                      "recommendations": recs}

        lines.append("")
        lines.append(f"JOB: {job_title}")
        lines.append(f"  Compatibility score : {result['score']}/100")
        lines.append(f"  Skill coverage      : {result['coverage']:.0%}"
                     f"  (cosine {result['cosine']:.3f}, "
                     f"beats {result['percentile']:.0%} of corpus)")
        lines.append(f"  Required matched    : "
                     f"{', '.join(result['matched_hard']) or '(none)'}")
        lines.append(f"  Required MISSING    : "
                     f"{', '.join(result['missing_hard']) or '(none)'}")
        lines.append(f"  Preferred matched   : "
                     f"{', '.join(result['matched_soft']) or '(none)'}")
        if recs:
            lines.append("  Top recommended edits (estimated score gain):")
            for r in recs:
                lines.append(f"    + {r['skill']:<20} [{r['kind']}]  +{r['gain']} pts")

    output = "\n".join(lines)
    print(output)

    (RESULTS / "demo_output.txt").write_text(output, encoding="utf-8")
    for key in all_results:
        all_results[key].pop("resume_skills", None)
    (RESULTS / "demo_results.json").write_text(
        json.dumps(all_results, indent=2), encoding="utf-8")

    # match score chart
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
        "text.color": INK, "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Arial"],
        "xtick.color": MUTED, "ytick.color": MUTED,
    })
    titles = [all_results[k]["title"].split(" - ")[0] for k in sorted(all_results)]
    scores = [all_results[k]["score"] for k in sorted(all_results)]
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    bars = ax.barh(titles, scores, color=BLUE, height=0.55)
    for rect, s in zip(bars, scores):
        ax.text(rect.get_width() + 1, rect.get_y() + rect.get_height() / 2,
                f"{s}", va="center", fontsize=10, color=INK)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Compatibility score (0-100)")
    ax.set_title("One IT resume matched against three job postings",
                 loc="left", fontsize=11, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig4_match_scores.png", dpi=200)
    plt.close(fig)

    render_text_figure(output, FIGURES / "fig5_demo_output.png")
    print("\nSaved demo artifacts to results/ and figures/")


if __name__ == "__main__":
    main()

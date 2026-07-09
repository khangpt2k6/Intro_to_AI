"""Train and evaluate the resume category classifiers, and produce the
figures and metrics used in the progress report.

Outputs:
  results/metrics.json          all numbers quoted in the report
  figures/fig1_category_distribution.png
  figures/fig2_model_comparison.png
  figures/fig3_confusion_matrix.png
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "resume-dataset" / "Resume.csv"
FIGURES = ROOT / "figures"
RESULTS = ROOT / "results"

# validated light-mode palette (dataviz reference instance)
BLUE = "#2a78d6"
AQUA = "#1baf7a"
INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"
SURFACE = "#fcfcfb"
SEQ_STEPS = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5",
             "#256abf", "#184f95", "#0d366b"]

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": INK, "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Arial"], "axes.grid": False,
})


def fig_category_distribution(df):
    counts = df["Category"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.barh(counts.index, counts.values, color=BLUE, height=0.62)
    ax.set_xlabel("Number of resumes")
    ax.set_title("Resume Dataset: 2,484 resumes across 24 job categories",
                 loc="left", fontsize=11, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    for i, v in enumerate(counts.values):
        ax.text(v + 1.5, i, str(v), va="center", fontsize=7.5, color=MUTED)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig1_category_distribution.png", dpi=200)
    plt.close(fig)


def fig_model_comparison(metrics):
    models = list(metrics.keys())
    acc = [metrics[m]["accuracy"] for m in models]
    f1 = [metrics[m]["macro_f1"] for m in models]
    x = np.arange(len(models))
    w = 0.32
    fig, ax = plt.subplots(figsize=(6.4, 4))
    b1 = ax.bar(x - w / 2, acc, w, label="Accuracy", color=BLUE)
    b2 = ax.bar(x + w / 2, f1, w, label="Macro F1", color=AQUA)
    for bars in (b1, b2):
        for rect in bars:
            ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 0.012,
                    f"{rect.get_height():.3f}", ha="center", fontsize=9, color=INK)
    ax.set_xticks(x, models)
    ax.set_ylim(0, 1.0)
    ax.set_title("Resume category classification, 20% held-out test set",
                 loc="left", fontsize=11, fontweight="bold")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig2_model_comparison.png", dpi=200)
    plt.close(fig)


def fig_confusion(cm, labels, model_name):
    cm_norm = cm / cm.sum(axis=1, keepdims=True)
    cmap = LinearSegmentedColormap.from_list("seq_blue", SEQ_STEPS)
    fig, ax = plt.subplots(figsize=(9, 8))
    im = ax.imshow(cm_norm, cmap=cmap, vmin=0, vmax=1)
    ax.set_xticks(range(len(labels)), labels, rotation=90, fontsize=7)
    ax.set_yticks(range(len(labels)), labels, fontsize=7)
    ax.set_xlabel("Predicted category")
    ax.set_ylabel("True category")
    ax.set_title(f"Normalized confusion matrix - {model_name}",
                 loc="left", fontsize=11, fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.7, label="Fraction of true class")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig3_confusion_matrix.png", dpi=200)
    plt.close(fig)


def main():
    FIGURES.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)

    df = pd.read_csv(DATA)
    print(f"Loaded {len(df)} resumes, {df['Category'].nunique()} categories")
    fig_category_distribution(df)

    X_train, X_test, y_train, y_test = train_test_split(
        df["Resume_str"], df["Category"], test_size=0.2,
        stratify=df["Category"], random_state=42,
    )

    models = {
        "Naive Bayes": Pipeline([
            ("tfidf", TfidfVectorizer(stop_words="english", max_features=20000,
                                      ngram_range=(1, 2), sublinear_tf=True)),
            ("clf", MultinomialNB(alpha=0.1)),
        ]),
        "Logistic Regression": Pipeline([
            ("tfidf", TfidfVectorizer(stop_words="english", max_features=20000,
                                      ngram_range=(1, 2), sublinear_tf=True)),
            ("clf", LogisticRegression(max_iter=2000, C=10.0)),
        ]),
    }

    metrics = {}
    best_name, best_acc, best_pred = None, -1.0, None
    for name, pipe in models.items():
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        acc = accuracy_score(y_test, pred)
        f1 = f1_score(y_test, pred, average="macro")
        metrics[name] = {"accuracy": round(acc, 4), "macro_f1": round(f1, 4)}
        print(f"{name}: accuracy={acc:.4f}  macro_f1={f1:.4f}")
        if acc > best_acc:
            best_name, best_acc, best_pred = name, acc, pred

    fig_model_comparison(metrics)

    labels = sorted(df["Category"].unique())
    cm = confusion_matrix(y_test, best_pred, labels=labels)
    fig_confusion(cm, labels, best_name)

    out = {
        "dataset": {
            "name": "Resume Dataset (Kaggle, snehaanbhawal/resume-dataset)",
            "n_resumes": int(len(df)),
            "n_categories": int(df["Category"].nunique()),
            "train_size": int(len(X_train)),
            "test_size": int(len(X_test)),
        },
        "models": metrics,
        "best_model": best_name,
    }
    (RESULTS / "metrics.json").write_text(json.dumps(out, indent=2))
    print(f"Saved metrics to {RESULTS / 'metrics.json'}")


if __name__ == "__main__":
    main()

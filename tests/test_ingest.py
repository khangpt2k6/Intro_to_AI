"""Resume ingestion: text normalization and file-type handling."""

from pathlib import Path

import pytest

from resume_matcher.ingest import load_resume

SAMPLES = Path(__file__).resolve().parent.parent / "sample_resumes"


def test_txt_is_normalized(tmp_path):
    messy = tmp_path / "r.txt"
    messy.write_text("Skills:\tPython   and    SQL\n\n\n  \nBuilt   APIs\n",
                     encoding="utf-8")
    text = load_resume(messy)
    assert "Python and SQL" in text          # runs of whitespace collapsed
    assert "\n\n" not in text                  # blank lines dropped
    assert text.splitlines() == ["Skills: Python and SQL", "Built APIs"]


def test_unicode_punctuation_folded(tmp_path):
    messy = tmp_path / "r.txt"
    messy.write_text("“Smart” quotes – and • bullets",
                     encoding="utf-8")
    text = load_resume(messy)
    assert "“" not in text and "–" not in text and "•" not in text


def test_unsupported_extension_raises(tmp_path):
    bad = tmp_path / "resume.rtf"
    bad.write_text("hi", encoding="utf-8")
    with pytest.raises(ValueError):
        load_resume(bad)


@pytest.mark.parametrize("name", ["jordan_rivera_resume.pdf",
                                  "jordan_rivera_resume.docx"])
def test_sample_files_load_nonempty(name):
    path = SAMPLES / name
    if not path.exists():
        pytest.skip(f"{name} not present")
    text = load_resume(path)
    assert isinstance(text, str) and len(text) > 20

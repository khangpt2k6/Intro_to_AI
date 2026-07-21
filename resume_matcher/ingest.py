"""Turn an uploaded resume file into clean text for the existing pipeline.

Supports the file types a real user would actually upload (PDF, DOCX) plus
plain text. Output is normalized the same way regardless of source format so
extract_skills() (resume_matcher/extraction.py) sees text shaped like the
CSV's Resume_str column, not raw PDF/DOCX layout artifacts.
"""

import re
import unicodedata
from pathlib import Path

from docx import Document
from pypdf import PdfReader

_WHITESPACE_RE = re.compile(r"[ \t]+")

# common non-ASCII punctuation from PDF/DOCX exports that would otherwise
# survive NFKD normalization (it only decomposes accented letters, not these)
_UNICODE_REPLACEMENTS = {
    "‘": "'", "’": "'",  # curly single quotes
    "“": '"', "”": '"',  # curly double quotes
    "–": "-", "—": "-",  # en/em dash
    "•": "-", "●": "-", "▪": "-", "◦": "-",  # bullets
}


def _normalize_text(text):
    for src, dst in _UNICODE_REPLACEMENTS.items():
        text = text.replace(src, dst)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    lines = (_WHITESPACE_RE.sub(" ", line).strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)


def _load_pdf(path):
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _load_docx(path):
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


def _load_txt(path):
    return Path(path).read_text(encoding="utf-8")


_LOADERS = {".pdf": _load_pdf, ".docx": _load_docx, ".txt": _load_txt}


def load_resume(path):
    """Extract clean text from a .pdf, .docx, or .txt resume file."""
    path = Path(path)
    loader = _LOADERS.get(path.suffix.lower())
    if loader is None:
        raise ValueError(
            f"Unsupported resume file type '{path.suffix}': "
            f"expected one of {sorted(_LOADERS)}"
        )
    return _normalize_text(loader(path))

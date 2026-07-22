"""Import smoke test.

The whole package - including matching.py, which uses Sentence-BERT - must
import without torch/sentence-transformers installed. semantic.py defers that
heavy import to first use; this test locks that in so a regression can't
silently make CI (and the web UI) require torch just to import.
"""

import sys


def test_package_imports_without_torch():
    import resume_matcher  # noqa: F401
    import resume_matcher.extraction  # noqa: F401
    import resume_matcher.matching  # noqa: F401
    import resume_matcher.recommendation  # noqa: F401
    import resume_matcher.semantic  # noqa: F401
    import resume_matcher.confidence  # noqa: F401

    # importing the package must not have eagerly pulled in the torch stack
    assert "sentence_transformers" not in sys.modules
    assert "torch" not in sys.modules

from pathlib import Path

from uncanny.bench.runner import run

CORPUS_DIR = Path(__file__).resolve().parent.parent / "benchmarks" / "corpus"


def test_accuracy_above_threshold():
    """Ensure accuracy doesn't regress below 70%."""
    report = run(corpus_dir=CORPUS_DIR)
    assert report.accuracy >= 0.7, f"Accuracy {report.accuracy:.1%} below 70% threshold"


def test_no_false_positives():
    """Human text should not be flagged as AI (false positive rate < 20%)."""
    report = run(corpus_dir=CORPUS_DIR)
    assert report.false_positive_rate < 0.2, (
        f"False positive rate {report.false_positive_rate:.1%} too high"
    )


def test_score_separation():
    """AI scores should be higher than human scores on average."""
    report = run(corpus_dir=CORPUS_DIR)
    assert report.separation > 0.1, (
        f"Score separation {report.separation:.2f} too low"
    )

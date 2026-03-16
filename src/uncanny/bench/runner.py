"""Benchmark runner for accuracy and performance testing."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

from uncanny.analyzers.base import Analyzer
from uncanny.analyzers.compression import CompressionAnalyzer
from uncanny.analyzers.burstiness import BurstinessAnalyzer
from uncanny import ensemble


@dataclass
class SampleResult:
    file: str
    label: str  # "ai" or "human"
    score: float
    correct: bool
    duration_ms: float
    per_analyzer: dict[str, float] = field(default_factory=dict)


@dataclass
class BenchmarkReport:
    samples: list[SampleResult]
    total_duration_ms: float
    analyzers_used: list[str]

    @property
    def accuracy(self) -> float:
        if not self.samples:
            return 0.0
        return sum(1 for s in self.samples if s.correct) / len(self.samples)

    @property
    def ai_samples(self) -> list[SampleResult]:
        return [s for s in self.samples if s.label == "ai"]

    @property
    def human_samples(self) -> list[SampleResult]:
        return [s for s in self.samples if s.label == "human"]

    @property
    def true_positive_rate(self) -> float:
        ai = self.ai_samples
        if not ai:
            return 0.0
        return sum(1 for s in ai if s.correct) / len(ai)

    @property
    def true_negative_rate(self) -> float:
        human = self.human_samples
        if not human:
            return 0.0
        return sum(1 for s in human if s.correct) / len(human)

    @property
    def false_positive_rate(self) -> float:
        human = self.human_samples
        if not human:
            return 0.0
        return sum(1 for s in human if not s.correct) / len(human)

    @property
    def avg_ai_score(self) -> float:
        ai = self.ai_samples
        return sum(s.score for s in ai) / len(ai) if ai else 0.0

    @property
    def avg_human_score(self) -> float:
        human = self.human_samples
        return sum(s.score for s in human) / len(human) if human else 0.0

    @property
    def separation(self) -> float:
        """Gap between average AI and human scores. Higher = better."""
        return self.avg_ai_score - self.avg_human_score

    @property
    def avg_ms_per_sample(self) -> float:
        if not self.samples:
            return 0.0
        return self.total_duration_ms / len(self.samples)

    def to_dict(self) -> dict:
        return {
            "accuracy": round(self.accuracy, 4),
            "true_positive_rate": round(self.true_positive_rate, 4),
            "true_negative_rate": round(self.true_negative_rate, 4),
            "false_positive_rate": round(self.false_positive_rate, 4),
            "avg_ai_score": round(self.avg_ai_score, 4),
            "avg_human_score": round(self.avg_human_score, 4),
            "separation": round(self.separation, 4),
            "total_duration_ms": round(self.total_duration_ms, 1),
            "avg_ms_per_sample": round(self.avg_ms_per_sample, 1),
            "analyzers": self.analyzers_used,
            "samples": [
                {
                    "file": s.file,
                    "label": s.label,
                    "score": round(s.score, 4),
                    "correct": s.correct,
                    "duration_ms": round(s.duration_ms, 1),
                    "per_analyzer": {
                        k: round(v, 4) for k, v in s.per_analyzer.items()
                    },
                }
                for s in self.samples
            ],
        }


def load_corpus(corpus_dir: Path) -> list[tuple[str, str, str]]:
    """Load corpus samples. Returns list of (text, label, filename)."""
    samples: list[tuple[str, str, str]] = []

    for label_dir in sorted(corpus_dir.iterdir()):
        if not label_dir.is_dir():
            continue
        label = label_dir.name  # "ai" or "human"
        for f in sorted(label_dir.iterdir()):
            if f.suffix == ".txt":
                text = f.read_text(encoding="utf-8").strip()
                if text:
                    samples.append((text, label, f.name))

    return samples


def build_analyzers(analyzer_names: list[str] | None = None) -> list[Analyzer]:
    """Build analyzer instances."""
    names = analyzer_names or ["compression", "burstiness"]
    analyzers: list[Analyzer] = []

    for name in names:
        if name == "compression":
            analyzers.append(CompressionAnalyzer())
        elif name == "burstiness":
            analyzers.append(BurstinessAnalyzer())
        elif name == "perplexity":
            from uncanny.analyzers.perplexity import PerplexityAnalyzer

            analyzers.append(PerplexityAnalyzer())

    return analyzers


def run(
    corpus_dir: Path,
    analyzer_names: list[str] | None = None,
    threshold: float = 0.5,
) -> BenchmarkReport:
    """Run accuracy + performance benchmarks against the corpus."""
    samples = load_corpus(corpus_dir)
    analyzers = build_analyzers(analyzer_names)

    results: list[SampleResult] = []
    total_start = time.perf_counter()

    for text, label, filename in samples:
        sample_start = time.perf_counter()

        analyzer_results = [a.analyze(text) for a in analyzers]
        scan_result = ensemble.combine(analyzer_results, source=filename)

        duration_ms = (time.perf_counter() - sample_start) * 1000

        if label == "ai":
            correct = scan_result.score >= threshold
        else:
            correct = scan_result.score < threshold

        per_analyzer = {ar.name: ar.score for ar in analyzer_results}

        results.append(
            SampleResult(
                file=filename,
                label=label,
                score=scan_result.score,
                correct=correct,
                duration_ms=duration_ms,
                per_analyzer=per_analyzer,
            )
        )

    total_ms = (time.perf_counter() - total_start) * 1000

    return BenchmarkReport(
        samples=results,
        total_duration_ms=total_ms,
        analyzers_used=[a.name for a in analyzers],
    )


# ---------------------------------------------------------------------------
# Competitor comparison
# ---------------------------------------------------------------------------

@dataclass
class CompetitorResult:
    name: str
    accuracy: float
    true_positive_rate: float
    true_negative_rate: float
    false_positive_rate: float
    avg_ai_score: float
    avg_human_score: float
    separation: float
    total_duration_ms: float
    avg_ms_per_sample: float


def run_competitors(
    corpus_dir: Path,
    threshold: float = 0.5,
) -> list[CompetitorResult]:
    """Run competitor algorithms against the same corpus."""
    from uncanny.bench.competitors import zippy_ensemble, naive_baseline

    samples = load_corpus(corpus_dir)
    results: list[CompetitorResult] = []

    competitors: list[tuple[str, object]] = [
        ("zippy", zippy_ensemble),
        ("random_baseline", naive_baseline),
    ]

    for comp_name, detect_fn in competitors:
        ai_scores: list[float] = []
        human_scores: list[float] = []
        correct = 0
        total = len(samples)
        start = time.perf_counter()

        for text, label, _filename in samples:
            if comp_name == "zippy":
                result = detect_fn(text)
                score = result.score
            else:
                score = detect_fn(text)

            if label == "ai":
                ai_scores.append(score)
                if score >= threshold:
                    correct += 1
            else:
                human_scores.append(score)
                if score < threshold:
                    correct += 1

        elapsed = (time.perf_counter() - start) * 1000

        avg_ai = sum(ai_scores) / len(ai_scores) if ai_scores else 0.0
        avg_human = sum(human_scores) / len(human_scores) if human_scores else 0.0
        tp = sum(1 for s in ai_scores if s >= threshold) / len(ai_scores) if ai_scores else 0.0
        tn = sum(1 for s in human_scores if s < threshold) / len(human_scores) if human_scores else 0.0
        fp = 1.0 - tn

        results.append(
            CompetitorResult(
                name=comp_name,
                accuracy=correct / total if total else 0.0,
                true_positive_rate=tp,
                true_negative_rate=tn,
                false_positive_rate=fp,
                avg_ai_score=avg_ai,
                avg_human_score=avg_human,
                separation=avg_ai - avg_human,
                total_duration_ms=elapsed,
                avg_ms_per_sample=elapsed / total if total else 0.0,
            )
        )

    return results

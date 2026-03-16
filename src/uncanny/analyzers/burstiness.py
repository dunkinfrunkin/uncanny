"""
Burstiness-based AI detection.

Measures variance in sentence complexity across a document.
Humans write with natural variation (short/long sentences, simple/complex ideas).
AI text is uniformly smooth.

Uses zlib compression ratio per-sentence as a proxy for complexity.
"""

from __future__ import annotations

import math
import zlib

from uncanny.analyzers.base import Analyzer
from uncanny.tokenizer import split_sentences
from uncanny.types import AnalyzerResult, SentenceScore


def _compress_ratio(data: bytes) -> float:
    """Compression ratio using zlib."""
    if len(data) == 0:
        return 1.0
    return len(zlib.compress(data, level=6)) / len(data)


def _variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return sum((v - mean) ** 2 for v in values) / (len(values) - 1)


def _burstiness_to_score(variance: float, length_cv: float) -> float:
    """Convert burstiness metrics to AI probability score.

    Low variance + low length CV = uniform = AI-like = high score.
    High variance + high length CV = bursty = human-like = low score.

    Calibrated from corpus:
      AI:    ratio_var mean=0.020, length_cv mean=0.41
      Human: ratio_var mean=0.041, length_cv mean=0.62
    """
    # Compression ratio variance signal
    # AI: 0.001-0.070, mean 0.020. Human: 0.003-0.079, mean 0.041.
    # Use sigmoid centered around 0.030 (midpoint)
    rv_centered = (variance - 0.030) * 60.0
    ratio_signal = 1.0 / (1.0 + math.exp(rv_centered))

    # Sentence length CV signal
    # AI: 0.17-1.12, mean 0.41. Human: 0.22-0.89, mean 0.62.
    # Use sigmoid centered around 0.50 (midpoint)
    lcv_centered = (length_cv - 0.50) * 4.0
    length_signal = 1.0 / (1.0 + math.exp(lcv_centered))

    return 0.55 * ratio_signal + 0.45 * length_signal


class BurstinessAnalyzer(Analyzer):
    """Detects AI text by measuring uniformity of sentence complexity."""

    name = "burstiness"

    def analyze(self, text: str) -> AnalyzerResult:
        sentences = split_sentences(text)

        if len(sentences) < 3:
            return AnalyzerResult(
                name=self.name,
                score=0.5,
                sentence_scores=[
                    SentenceScore(s, 0.5, start, end) for s, start, end in sentences
                ],
                metadata={"variance": 0.0, "note": "too few sentences"},
            )

        # Compression ratio per sentence as complexity proxy
        ratios: list[float] = []
        for sent_text, _, _ in sentences:
            if len(sent_text.strip()) < 10:
                continue
            ratios.append(_compress_ratio(sent_text.encode("utf-8")))

        if len(ratios) < 3:
            return AnalyzerResult(
                name=self.name,
                score=0.5,
                sentence_scores=[
                    SentenceScore(s, 0.5, start, end) for s, start, end in sentences
                ],
                metadata={"variance": 0.0, "note": "too few analyzable sentences"},
            )

        # Sentence length variance
        lengths = [len(s.split()) for s, _, _ in sentences]
        mean_length = sum(lengths) / len(lengths)
        length_cv = math.sqrt(_variance(lengths)) / max(mean_length, 1)

        ratio_var = _variance(ratios)
        overall_score = _burstiness_to_score(ratio_var, length_cv)

        # Per-sentence: deviation from mean indicates human-like variety
        mean_ratio = sum(ratios) / len(ratios)
        sentence_scores: list[SentenceScore] = []
        ratio_idx = 0
        for sent_text, start, end in sentences:
            if len(sent_text.strip()) < 10:
                sentence_scores.append(SentenceScore(sent_text, 0.5, start, end))
                continue
            deviation = abs(ratios[ratio_idx] - mean_ratio)
            sent_score = max(0.0, min(1.0, 1.0 - deviation * 15))
            sentence_scores.append(SentenceScore(sent_text, sent_score, start, end))
            ratio_idx += 1

        return AnalyzerResult(
            name=self.name,
            score=overall_score,
            sentence_scores=sentence_scores,
            metadata={"variance": round(ratio_var, 6), "length_cv": round(length_cv, 3)},
        )

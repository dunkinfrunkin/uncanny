"""Ensemble scorer that combines multiple analyzer results."""

from __future__ import annotations

from uncanny.types import AnalyzerResult, ScanResult, SentenceScore

# Default weights for each analyzer.
# Compression is the primary signal. Burstiness acts as a tiebreaker —
# it gets more weight when compression is ambiguous (0.4-0.6 range).
DEFAULT_WEIGHTS: dict[str, float] = {
    "compression": 0.65,
    "perplexity": 0.35,
    "burstiness": 0.20,
}


def _score_label(score: float) -> str:
    if score >= 0.85:
        return "ai_generated"
    if score >= 0.65:
        return "likely_ai"
    if score >= 0.45:
        return "mixed"
    if score >= 0.25:
        return "likely_human"
    return "human"


def _dynamic_weight(
    base_weight: float,
    name: str,
    compression_score: float | None,
) -> float:
    """Adjust burstiness weight based on how confident compression is.

    When compression is decisive (far from 0.5), burstiness gets less weight.
    When compression is ambiguous (near 0.5), burstiness gets full weight.
    """
    if name != "burstiness" or compression_score is None:
        return base_weight

    # How far is compression from the decision boundary?
    confidence = abs(compression_score - 0.5) * 2  # 0 = ambiguous, 1 = decisive

    # Scale burstiness weight: full weight when ambiguous, reduced when decisive
    return base_weight * (1.0 - confidence * 0.6)


def combine(
    results: list[AnalyzerResult],
    source: str | None = None,
    weights: dict[str, float] | None = None,
) -> ScanResult:
    """Combine multiple analyzer results into a single scan result."""
    w = weights or DEFAULT_WEIGHTS

    # Find compression score for dynamic weighting
    compression_score = None
    for result in results:
        if result.name == "compression":
            compression_score = result.score
            break

    # Weighted average for overall score
    total_weight = 0.0
    weighted_score = 0.0
    analyzers: dict[str, AnalyzerResult] = {}

    for result in results:
        base_w = w.get(result.name, 0.3)
        weight = _dynamic_weight(base_w, result.name, compression_score)
        weighted_score += result.score * weight
        total_weight += weight
        analyzers[result.name] = result

    overall = weighted_score / total_weight if total_weight > 0 else 0.5

    # Combine sentence scores across analyzers
    sentence_map: dict[tuple[int, int], list[tuple[float, float]]] = {}
    sentence_text: dict[tuple[int, int], str] = {}

    for result in results:
        base_w = w.get(result.name, 0.3)
        weight = _dynamic_weight(base_w, result.name, compression_score)
        for ss in result.sentence_scores:
            key = (ss.start, ss.end)
            if key not in sentence_map:
                sentence_map[key] = []
                sentence_text[key] = ss.text
            sentence_map[key].append((ss.score, weight))

    sentences: list[SentenceScore] = []
    for key in sorted(sentence_map.keys()):
        pairs = sentence_map[key]
        tw = sum(p[1] for p in pairs)
        ws = sum(p[0] * p[1] for p in pairs) / tw if tw > 0 else 0.5
        sentences.append(SentenceScore(sentence_text[key], ws, key[0], key[1]))

    return ScanResult(
        source=source,
        score=overall,
        label=_score_label(overall),
        analyzers=analyzers,
        sentences=sentences,
    )

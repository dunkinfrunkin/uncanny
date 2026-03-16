"""Ensemble scorer that combines multiple analyzer results."""

from __future__ import annotations

from uncanny.types import AnalyzerResult, ScanResult, SentenceScore

# Default weights for each analyzer
DEFAULT_WEIGHTS: dict[str, float] = {
    "compression": 0.55,
    "perplexity": 0.35,
    "burstiness": 0.25,
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


def combine(
    results: list[AnalyzerResult],
    source: str | None = None,
    weights: dict[str, float] | None = None,
) -> ScanResult:
    """Combine multiple analyzer results into a single scan result."""
    w = weights or DEFAULT_WEIGHTS

    # Weighted average for overall score
    total_weight = 0.0
    weighted_score = 0.0
    analyzers: dict[str, AnalyzerResult] = {}

    for result in results:
        weight = w.get(result.name, 0.3)  # default weight for unknown analyzers
        weighted_score += result.score * weight
        total_weight += weight
        analyzers[result.name] = result

    overall = weighted_score / total_weight if total_weight > 0 else 0.5

    # Combine sentence scores across analyzers
    # Group by (start, end) offset to align sentences
    sentence_map: dict[tuple[int, int], list[tuple[float, float]]] = {}
    sentence_text: dict[tuple[int, int], str] = {}

    for result in results:
        weight = w.get(result.name, 0.3)
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

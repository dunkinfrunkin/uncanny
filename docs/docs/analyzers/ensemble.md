---
sidebar_position: 5
title: Ensemble Scoring
---

# Ensemble Scoring

Uncanny combines multiple analyzer signals through a **confidence-aware dynamic weighting** system.

## Why Not Just Average?

Simple averaging treats all signals equally. But in practice:
- The compression analyzer is the **strongest single signal**
- Burstiness is noisy and can override a correct compression call
- A weak signal shouldn't drag down a strong one

## How Dynamic Weighting Works

### Base Weights

| Analyzer | Base Weight |
|----------|:----------:|
| Compression | 0.65 |
| Perplexity | 0.35 |
| Burstiness | 0.20 |

### Confidence-Aware Adjustment

When compression is **confident** (far from 0.5), burstiness weight is reduced:

```
confidence = |compression_score - 0.5| * 2    # 0 = ambiguous, 1 = decisive
burstiness_weight = base_weight * (1 - confidence * 0.6)
```

**Example**: If compression scores 0.85 (confident AI):
- Confidence = |0.85 - 0.5| * 2 = 0.70
- Burstiness weight = 0.20 * (1 - 0.70 * 0.6) = 0.20 * 0.58 = 0.116

This means burstiness can only nudge the score slightly when compression already has a strong opinion.

**When compression is ambiguous** (score ~0.50):
- Confidence = ~0
- Burstiness gets full weight (0.20)
- This is when the tiebreaker actually matters

## Per-Sentence Scoring

The same weighting applies to individual sentences. Each sentence gets a weighted average score across all analyzers.

## Custom Weights

You can pass custom weights programmatically:

```python
from uncanny.ensemble import combine

result = combine(
    analyzer_results,
    weights={"compression": 0.8, "burstiness": 0.1, "perplexity": 0.5},
)
```

## Score Labels

| Score Range | Label |
|-------------|-------|
| 0.85 - 1.00 | `ai_generated` |
| 0.65 - 0.84 | `likely_ai` |
| 0.45 - 0.64 | `mixed` |
| 0.25 - 0.44 | `likely_human` |
| 0.00 - 0.24 | `human` |

## Implementation

Source: [`src/uncanny/ensemble.py`](https://github.com/dunkinfrunkin/uncanny/blob/main/src/uncanny/ensemble.py)

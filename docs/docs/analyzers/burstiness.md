---
sidebar_position: 3
title: Burstiness
---

# Burstiness Analyzer

Measures the variance in sentence complexity across a document. Humans write with natural variation; AI is uniformly smooth.

## How It Works

1. **Compute per-sentence compression ratios** — each sentence's compression ratio acts as a proxy for its complexity
2. **Measure variance** — calculate the variance of these ratios across all sentences
3. **Measure sentence length CV** — coefficient of variation of sentence word counts
4. **Score** — low variance + low length CV = AI-like uniformity

## The Intuition

Human writing is **bursty**:
- Short punchy sentences mixed with long complex ones
- Simple ideas next to technical depth
- Informal asides interrupting formal arguments

AI writing is **uniform**:
- Consistent sentence length
- Even complexity throughout
- Smooth transitions, no tonal shifts

## Signal Calibration

Calibrated from the 36-sample benchmark corpus:

| Metric | AI (mean) | Human (mean) |
|--------|:---------:|:------------:|
| Compression ratio variance | 0.020 | 0.041 |
| Sentence length CV | 0.41 | 0.62 |

Both signals use sigmoid functions centered at the midpoints for smooth scoring.

## Role in Ensemble

Burstiness acts as a **tiebreaker**, not an equal partner. Its weight is dynamically reduced when the compression analyzer is confident. This prevents burstiness from overriding a strong compression signal.

## Limitations

- Requires **3+ sentences** to produce a meaningful signal (returns 0.5 for shorter text)
- Text with naturally uniform structure (lists, bullet points) may score higher
- Less reliable than compression as a standalone signal

## Implementation

Source: [`src/uncanny/analyzers/burstiness.py`](https://github.com/dunkinfrunkin/uncanny/blob/main/src/uncanny/analyzers/burstiness.py)

---
sidebar_position: 2
title: Compression
---

# Compression Analyzer

The primary detection signal. Uses cross-compression to detect AI-generated text patterns.

## How It Works

AI text is statistically predictable — it uses common phrases, uniform structure, and high-frequency token patterns. This means it **compresses better** when combined with other AI text.

The algorithm:

1. **Prepare two preludes**: a large block of known AI-generated text and a large block of known human-written text
2. **Cross-compress**: compress `(AI prelude + sample)` and `(human prelude + sample)` using both LZMA and zlib
3. **Compare deltas**: if the sample adds fewer bytes to the AI prelude, it shares statistical patterns with AI text
4. **Amplify**: apply a sigmoid function to stretch the subtle signal into a usable 0-1 score

## Why Two Compressors?

LZMA and zlib use different compression algorithms with different dictionary approaches. Using both provides two independent signals that are averaged together, reducing noise.

## Strengths

- **Zero dependencies** — uses Python's built-in `lzma` and `zlib` modules
- **Fast** — ~2ms per sample
- **Most reliable single signal** — best standalone accuracy
- **Works on any text length** — though more reliable on longer text

## Weaknesses

- **Subtle signal** — raw cross-compression differences are small (typically 0.48 vs 0.52), requiring amplification
- **Prelude-dependent** — accuracy depends on the quality and diversity of the prelude text
- **Technical writing bias** — formal, structured writing can false-positive slightly

## Configuration

```bash
# Use compression only (fastest mode)
uncanny scan report.md --fast

# Or explicitly
uncanny scan report.md --analyzers compression
```

## Implementation

Source: [`src/uncanny/analyzers/compression.py`](https://github.com/dunkinfrunkin/uncanny/blob/main/src/uncanny/analyzers/compression.py)

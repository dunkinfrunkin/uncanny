---
sidebar_position: 1
title: Overview
---

# Analyzers

Uncanny uses multiple detection strategies, each implemented as an **analyzer**. Analyzers run independently and produce per-sentence scores (0.0 = human, 1.0 = AI). The [ensemble scorer](/analyzers/ensemble) combines them.

## Available Analyzers

| Analyzer | Dependencies | Speed | Signal Strength |
|----------|-------------|-------|----------------|
| [Compression](/analyzers/compression) | None (stdlib) | ~2ms | Primary |
| [Burstiness](/analyzers/burstiness) | None (stdlib) | ~1ms | Tiebreaker |
| [Perplexity](/analyzers/perplexity) | `torch`, `transformers` | ~200ms | Strong (optional) |

## Default Behavior

```bash
# Default: compression + burstiness (no downloads needed)
uncanny scan report.md

# Fast: compression only
uncanny scan report.md --fast

# Deep: all analyzers (needs uncanny[ml])
uncanny scan report.md --deep

# Pick specific analyzers
uncanny scan report.md --analyzers compression,burstiness
```

## Writing a Custom Analyzer

Every analyzer extends the `Analyzer` base class:

```python
from uncanny.analyzers.base import Analyzer
from uncanny.types import AnalyzerResult, SentenceScore
from uncanny.tokenizer import split_sentences


class MyAnalyzer(Analyzer):
    name = "my_analyzer"

    def analyze(self, text: str) -> AnalyzerResult:
        sentences = split_sentences(text)
        sentence_scores = []

        for sent_text, start, end in sentences:
            score = your_detection_logic(sent_text)
            sentence_scores.append(
                SentenceScore(sent_text, score, start, end)
            )

        overall = sum(s.score for s in sentence_scores) / len(sentence_scores)

        return AnalyzerResult(
            name=self.name,
            score=overall,
            sentence_scores=sentence_scores,
            metadata={"your_key": "your_value"},
        )
```

Then register it in `analyzers/__init__.py` and `cli.py`.

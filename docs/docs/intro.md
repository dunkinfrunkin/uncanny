---
slug: /
sidebar_position: 1
title: Introduction
---

# Uncanny

**Detect AI-generated text from your terminal.** Sentence-level scoring, multiple detection strategies, zero API calls. Runs locally, works offline, open source.

## What is Uncanny?

Uncanny is a CLI tool that analyzes text and tells you how likely it was written by AI. It gives you:

- **An overall score** (0.0 = human, 1.0 = AI) for the entire document
- **Per-sentence scores** so you can see exactly which parts triggered detection
- **Multiple detection strategies** combined through an ensemble scorer
- **JSON output** for piping into other tools and CI pipelines

## Why Uncanny?

Every other AI detector is a SaaS product that sends your text to someone else's server. Uncanny runs **entirely on your machine**.

| Feature | Uncanny | GPTZero | Originality.ai | Zippy |
|---------|:-------:|:-------:|:--------------:|:-----:|
| Open Source | Yes | No | No | Yes |
| Runs Offline | Yes | No | No | Yes |
| Sentence-Level | Yes | Yes | Yes | No |
| Multi-Method | Yes | Yes | Yes | No |
| CLI | Yes | No | No | Yes |

## Quick Example

```bash
$ uncanny scan --text "The implementation of this feature requires careful consideration of several architectural patterns to ensure maintainability and scalability."
0.85 (ai_generated)
```

```bash
$ uncanny scan --text "I tried like three approaches before landing on this one, honestly the code is ugly but it works."
0.28 (likely_human)
```

## Performance

Tested against 36 labeled samples across diverse genres:

| Metric | Uncanny | Zippy |
|--------|:-------:|:-----:|
| **Accuracy** | **91.7%** | 80.6% |
| False Positive Rate | **5.6%** | 38.9% |
| Speed | 8ms/sample | 1ms/sample |

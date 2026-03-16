---
sidebar_position: 7
title: Benchmarks
---

# Benchmarks

Uncanny ships with a built-in benchmark suite that tests accuracy and performance against a labeled corpus.

## Results

Tested against 36 labeled samples (18 AI-generated, 18 human-written):

| Metric | Uncanny | Zippy | Random Baseline |
|--------|:-------:|:-----:|:---------------:|
| **Accuracy** | **91.7%** | 80.6% | 50.0% |
| AI Detected (TP) | 88.9% | 100% | 100% |
| Human Cleared (TN) | **94.4%** | 61.1% | 0% |
| **False Positive Rate** | **5.6%** | 38.9% | 100% |
| Speed | 8ms/sample | 1ms/sample | 0ms |

:::info
**Uncanny beats Zippy by 11 points on accuracy** with 7x fewer false accusations. Zippy catches everything but wrongly flags 39% of human text.
:::

## Run Benchmarks

```bash
# Standard benchmark
uncanny bench

# Head-to-head vs competitors
uncanny bench --compare

# JSON output
uncanny bench --compare --json

# Test specific analyzers
uncanny bench --analyzers compression
```

## Corpus

The benchmark corpus includes 36 samples across diverse genres:

### AI Samples (18)
Academic paper, blog post, code review, cover letter, creative fiction, documentation, email response, essay, LinkedIn post, news article, PR description, product description, short response, Slack message, executive summary, technical doc, tutorial, casual-prompted AI

### Human Samples (18)
Slack message, personal essay, code review, casual email, forum post, Reddit rant, journal entry, text messages, personal blog, meeting notes, tweet thread, commit messages, debug notes, recipe review, standup update, technical/academic writing, short email, polished prose

### Adversarial Cases
The corpus deliberately includes hard cases:
- **Casual AI** — AI prompted to sound informal
- **Formal humans** — academic writing that looks AI-like
- **Short text** — 2-3 sentences where signal is weakest

## CI Regression Tests

Accuracy is enforced in CI via `tests/test_bench.py`:

```python
def test_accuracy_above_threshold():
    report = run(corpus_dir=CORPUS_DIR)
    assert report.accuracy >= 0.7

def test_no_false_positives():
    report = run(corpus_dir=CORPUS_DIR)
    assert report.false_positive_rate < 0.2

def test_score_separation():
    report = run(corpus_dir=CORPUS_DIR)
    assert report.separation > 0.1
```

Every PR must pass these gates.

## Bring Your Own Corpus

```bash
# Use a custom corpus directory
uncanny bench --corpus ./my-corpus

# Directory structure:
# my-corpus/
# ├── ai/
# │   ├── sample1.txt
# │   └── sample2.txt
# └── human/
#     ├── sample3.txt
#     └── sample4.txt
```

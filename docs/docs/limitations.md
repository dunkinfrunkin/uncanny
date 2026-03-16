---
sidebar_position: 9
title: Limitations
---

# Limitations

AI detection is an imperfect science. Uncanny is transparent about what it can and can't do.

## No Detector is 100% Accurate

False positives (flagging human text) and false negatives (missing AI text) are inevitable. Uncanny reports **probabilities**, never binary verdicts. The tool informs — it doesn't judge.

## Short Text is Unreliable

Detection confidence drops significantly below ~250 words. With only 2-3 sentences, there isn't enough statistical signal for reliable classification. Scores on short text should be treated as rough estimates.

## Edited AI Text is Harder to Detect

A human editing AI output blurs the signal. If someone generates a draft with ChatGPT and then rewrites half of it, the result is genuinely mixed-authorship text. Uncanny's per-sentence scoring helps here — you may see some sentences score high and others low.

## Newer Models Are Harder to Detect

As LLMs improve, their output becomes more statistically similar to human text. Detection methods that work well against GPT-3.5 may be less effective against GPT-4, Claude, or future models. This is an arms race.

## Technical Writing May False-Positive

Formal, structured writing (academic papers, technical documentation, legal text) shares some statistical properties with AI text: uniform sentence structure, conventional phrasing, predictable vocabulary. Uncanny's false positive rate on our benchmark is 5.6%, and most false positives come from formal human writing.

## Non-English Text

Uncanny is currently calibrated for English text only. The compression analyzer may work on other languages but has not been tested or calibrated for them. The perplexity analyzer uses GPT-2, which is primarily English-trained.

## What Uncanny is NOT

- **Not a plagiarism detector** — it detects AI patterns, not copied content
- **Not admissible evidence** — no AI detector should be used as sole evidence of misconduct
- **Not a content filter** — it's an analysis tool, not a gatekeeper

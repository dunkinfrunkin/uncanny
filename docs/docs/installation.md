---
sidebar_position: 2
title: Installation
---

# Installation

## Homebrew (recommended)

```bash
brew tap dunkinfrunkin/tap
brew install uncanny
```

## pip

```bash
pip install uncanny
```

## pipx (isolated install)

```bash
pipx install uncanny
```

## From source

```bash
git clone https://github.com/dunkinfrunkin/uncanny.git
cd uncanny
pip install -e ".[dev]"
```

## Optional: ML Dependencies

For the perplexity analyzer (`--deep` mode), install ML dependencies:

```bash
pip install "uncanny[ml]"
```

This downloads `torch` and `transformers` (~2GB). The perplexity analyzer uses GPT-2 small (~500MB model, downloaded on first use).

:::tip
The default analyzers (compression + burstiness) require **zero additional downloads** and work instantly. Only install ML deps if you want `--deep` mode.
:::

## Verify Installation

```bash
uncanny --version
# uncanny 0.1.0

uncanny scan --text "Hello world" --format summary
# 0.38 (likely_human)
```

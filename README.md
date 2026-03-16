# Uncanny

A CLI tool that detects AI-generated text with sentence-level scoring and multiple detection strategies.

## Install

```bash
pip install uncanny
```

For ML-based analyzers (perplexity):

```bash
pip install uncanny[ml]
```

## Usage

```bash
# Scan a file
uncanny scan report.md

# Scan from stdin
cat essay.txt | uncanny scan

# Scan a string
uncanny scan --text "The implementation of this feature..."

# Output formats
uncanny scan report.md --format json
uncanny scan report.md --format summary

# Fast mode (compression only, instant)
uncanny scan report.md --fast

# Deep mode (all analyzers including perplexity)
uncanny scan report.md --deep

# CI mode (exit code 1 if score > threshold)
uncanny scan report.md --threshold 0.7
```

## How It Works

Uncanny combines multiple detection strategies:

- **Compression analysis** — AI text is more predictable and compresses better than human text (Zippy-style)
- **Burstiness analysis** — AI text has uniform sentence complexity; humans vary naturally
- **Perplexity analysis** — measures how "surprised" a language model is by the text (requires `uncanny[ml]`)

Each analyzer produces per-sentence scores (0.0 = human, 1.0 = AI). An ensemble scorer combines them with configurable weights.

## License

MIT

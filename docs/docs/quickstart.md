---
sidebar_position: 3
title: Quickstart
---

# Quickstart

## Scan a file

```bash
uncanny scan report.md
```

## Scan a string

```bash
uncanny scan --text "The implementation of this feature requires careful consideration."
```

## Scan from stdin

```bash
cat essay.txt | uncanny scan
echo "some text" | uncanny scan
```

## Output formats

```bash
# Rich terminal output (default)
uncanny scan report.md

# JSON (for scripting/piping)
uncanny scan report.md --format json

# Just the score (for quick checks)
uncanny scan report.md --format summary
# 0.73 (likely_ai)
```

## Speed vs Depth

```bash
# Fast mode — compression only, instant, no model needed
uncanny scan report.md --fast

# Default — compression + burstiness (~8ms)
uncanny scan report.md

# Deep — all analyzers including perplexity (requires uncanny[ml])
uncanny scan report.md --deep
```

## Choose specific analyzers

```bash
uncanny scan report.md --analyzers compression
uncanny scan report.md --analyzers compression,burstiness
```

## CI mode

Exit code 1 if the AI probability exceeds your threshold:

```bash
uncanny scan submission.md --threshold 0.7
echo $?  # 1 if score > 0.7, 0 otherwise
```

## Web visualizer

Launch a local web UI with sentence and word-level heatmaps:

```bash
uncanny serve
# Opens browser at http://127.0.0.1:7272
```

## Run benchmarks

```bash
uncanny bench                  # accuracy benchmarks
uncanny bench --compare        # head-to-head vs competitors
uncanny bench --compare --json # machine-readable
```

---
sidebar_position: 4
title: CLI Reference
---

# CLI Reference

## `uncanny scan`

Analyze text for AI-generated content.

```
uncanny scan [FILE] [OPTIONS]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `FILE` | Path to a text file to scan (optional) |

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--text` | `-t` | — | Text string to scan directly |
| `--format` | `-f` | `terminal` | Output format: `terminal`, `json`, `summary` |
| `--fast` | — | `false` | Compression only (instant, no model needed) |
| `--deep` | — | `false` | All analyzers including perplexity |
| `--analyzers` | `-a` | — | Comma-separated analyzer names |
| `--threshold` | — | — | Exit code 1 if score exceeds threshold |

### Input Priority

1. `--text` flag (highest priority)
2. `FILE` argument
3. stdin (if piped)

### Examples

```bash
# Scan a file
uncanny scan report.md

# Scan a string
uncanny scan --text "Your text here"

# Pipe from stdin
cat essay.txt | uncanny scan

# JSON output
uncanny scan report.md --format json

# CI gate
uncanny scan report.md --threshold 0.7
```

---

## `uncanny bench`

Run accuracy and performance benchmarks.

```
uncanny bench [OPTIONS]
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--corpus` | `-c` | built-in | Path to corpus directory |
| `--analyzers` | `-a` | default | Comma-separated analyzer names |
| `--threshold` | — | `0.5` | Score threshold for classification |
| `--json` | — | `false` | Output results as JSON |
| `--compare` | — | `false` | Include competitor comparison |

### Examples

```bash
uncanny bench
uncanny bench --compare
uncanny bench --compare --json
uncanny bench --analyzers compression
uncanny bench --corpus ./my-corpus
```

---

## `uncanny serve`

Launch the web visualizer for interactive analysis.

```
uncanny serve [OPTIONS]
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--port` | `-p` | `7272` | Port to serve on |
| `--no-open` | — | `false` | Don't auto-open browser |

### Examples

```bash
uncanny serve
uncanny serve --port 8080
uncanny serve --no-open
```

---

## `uncanny version`

Show the installed version.

```bash
uncanny version
uncanny --version
uncanny -V
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success (or score below threshold) |
| `1` | Score exceeds `--threshold` value |
| `1` | Error (file not found, invalid input, etc.) |

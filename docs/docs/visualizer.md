---
sidebar_position: 6
title: Web Visualizer
---

# Web Visualizer

Uncanny includes a local web UI for interactive text analysis with visual heatmaps.

## Launch

```bash
uncanny serve
```

This opens `http://127.0.0.1:7272` in your browser.

### Options

```bash
uncanny serve --port 8080   # custom port
uncanny serve --no-open     # don't auto-open browser
```

## Features

### Score Ring
Animated circular indicator showing overall AI probability with color coding.

### Per-Analyzer Bars
Breakdown of each analyzer's individual score with progress bars.

### Sentence Heatmap
Each sentence is color-coded:
- **Red** (0.8+) — high AI probability
- **Yellow** (0.5-0.8) — mixed signals
- **Green** (below 0.5) — likely human

### Word-Level Heatmap
Every word is highlighted based on its sentence's score. Hover over any word to see the exact sentence score in a tooltip.

### Example Text
Click "Load Example" to try a mixed AI/human text sample.

## How It Works

- The frontend is static HTML/CSS/JS (no build step, no framework)
- `uncanny serve` starts a local Python HTTP server
- The `POST /api/analyze` endpoint runs the same analysis engine as the CLI
- All processing happens locally — no data leaves your machine

## Keyboard Shortcuts

- **Ctrl+Enter** / **Cmd+Enter** — Analyze text

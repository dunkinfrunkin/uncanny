"""Rich terminal output for scan results."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from uncanny.types import ScanResult

console = Console()


def _score_color(score: float) -> str:
    if score >= 0.8:
        return "red"
    if score >= 0.5:
        return "yellow"
    return "green"


def _score_bar(score: float, width: int = 20) -> str:
    filled = round(score * width)
    return "\u2588" * filled + "\u2591" * (width - filled)


def _level_label(score: float) -> str:
    if score >= 0.8:
        return "high"
    if score >= 0.5:
        return "moderate"
    return "low"


def _label_display(label: str) -> str:
    return {
        "ai_generated": "AI-generated",
        "likely_ai": "likely AI-generated",
        "mixed": "mixed signals",
        "likely_human": "likely human-written",
        "human": "human-written",
    }.get(label, label)


def render(result: ScanResult) -> None:
    """Render a scan result to the terminal."""
    source = result.source or "stdin"

    console.print()

    # Header
    header = Text()
    header.append("Uncanny Analysis", style="bold")
    header.append(f" \u2014 {source}", style="dim")
    console.print(header)
    console.print("\u2500" * 50, style="dim")
    console.print()

    # Overall score
    color = _score_color(result.score)
    console.print(
        f"  Overall Score: [{color} bold]{result.score:.2f}[/] "
        f"({_label_display(result.label)})"
    )
    console.print()
    pct = round(result.score * 100)
    bar = _score_bar(result.score, 30)
    console.print(f"  [{color}]{bar}[/]  {pct}% AI probability")
    console.print()

    # Per-analyzer breakdown
    if result.analyzers:
        console.print("  [bold]Analyzers:[/]")
        for name, ar in result.analyzers.items():
            ac = _score_color(ar.score)
            abar = _score_bar(ar.score, 10)
            meta = ""
            if "method" in ar.metadata:
                meta = f"  ({ar.metadata['method']})"
            if "model" in ar.metadata:
                meta = f"  ({ar.metadata['model']})"
            console.print(
                f"    {name:<14s} [{ac}]{ar.score:.2f}  {abar}[/]"
                f"  {_level_label(ar.score)}{meta}"
            )
        console.print()

    # Sentence breakdown
    if result.sentences:
        console.print("  [bold]Sentence Breakdown:[/]")
        for ss in result.sentences:
            sc = _score_color(ss.score)
            # Wrap long sentences
            lines = _wrap_text(ss.text, width=55)
            console.print(f"   [{sc}]{ss.score:.2f}[/] \u2502 {lines[0]}")
            for line in lines[1:]:
                console.print(f"        \u2502 {line}")
        console.print()

    # Legend
    console.print(
        "  Legend: [red]\u25a0 0.8+ AI[/]  "
        "[yellow]\u25a0 0.5-0.8 mixed[/]  "
        "[green]\u25a0 <0.5 human[/]"
    )
    console.print()


def _wrap_text(text: str, width: int = 55) -> list[str]:
    """Simple word wrap."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        if current and len(current) + len(word) + 1 > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}" if current else word
    if current:
        lines.append(current)
    return lines or [""]

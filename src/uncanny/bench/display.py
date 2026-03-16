"""Rich terminal display for benchmark results."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from uncanny.bench.runner import BenchmarkReport, CompetitorResult

console = Console()


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _score_color(score: float) -> str:
    if score >= 0.8:
        return "red"
    if score >= 0.5:
        return "yellow"
    return "green"


def render(report: BenchmarkReport) -> None:
    """Render benchmark report to terminal."""
    console.print()
    console.print("[bold]Uncanny Benchmark Results[/]")
    console.print("\u2500" * 60, style="dim")
    console.print()

    # Summary
    console.print("[bold]Summary[/]")
    console.print(f"  Analyzers:        {', '.join(report.analyzers_used)}")
    console.print(f"  Samples:          {len(report.samples)} ({len(report.ai_samples)} AI, {len(report.human_samples)} human)")
    console.print(f"  Total time:       {report.total_duration_ms:.0f}ms")
    console.print(f"  Avg per sample:   {report.avg_ms_per_sample:.1f}ms")
    console.print()

    # Accuracy
    acc_color = "green" if report.accuracy >= 0.8 else "yellow" if report.accuracy >= 0.6 else "red"
    console.print("[bold]Accuracy[/]")
    console.print(f"  Overall:          [{acc_color}]{_pct(report.accuracy)}[/]")
    console.print(f"  True positive:    {_pct(report.true_positive_rate)}  (AI correctly detected)")
    console.print(f"  True negative:    {_pct(report.true_negative_rate)}  (human correctly cleared)")
    console.print(f"  False positive:   {_pct(report.false_positive_rate)}  (human flagged as AI)")
    console.print()

    # Score distribution
    console.print("[bold]Score Distribution[/]")
    console.print(f"  Avg AI score:     {report.avg_ai_score:.2f}")
    console.print(f"  Avg human score:  {report.avg_human_score:.2f}")
    sep_color = "green" if report.separation >= 0.3 else "yellow" if report.separation >= 0.15 else "red"
    console.print(f"  Separation:       [{sep_color}]{report.separation:.2f}[/]  (higher = better discrimination)")
    console.print()

    # Per-sample table
    table = Table(title="Per-Sample Results", show_lines=False)
    table.add_column("File", style="cyan", max_width=25)
    table.add_column("Label", width=6)
    table.add_column("Score", width=6, justify="right")
    for name in report.analyzers_used:
        table.add_column(name[:10], width=8, justify="right")
    table.add_column("Result", width=8)
    table.add_column("Time", width=8, justify="right")

    for s in report.samples:
        label_style = "red" if s.label == "ai" else "green"
        score_style = _score_color(s.score)
        result_text = "[green]\u2713[/]" if s.correct else "[red]\u2717[/]"

        row = [
            s.file,
            f"[{label_style}]{s.label}[/]",
            f"[{score_style}]{s.score:.2f}[/]",
        ]
        for name in report.analyzers_used:
            a_score = s.per_analyzer.get(name, 0.0)
            row.append(f"{a_score:.2f}")
        row.append(result_text)
        row.append(f"{s.duration_ms:.0f}ms")

        table.add_row(*row)

    console.print(table)
    console.print()


def render_comparison(
    report: BenchmarkReport,
    competitors: list[CompetitorResult],
) -> None:
    """Render head-to-head comparison table."""
    console.print("[bold]Competitor Comparison[/]")
    console.print("\u2500" * 60, style="dim")
    console.print()

    table = Table(show_lines=True)
    table.add_column("Tool", style="bold", width=18)
    table.add_column("Accuracy", width=10, justify="right")
    table.add_column("TP Rate", width=10, justify="right")
    table.add_column("TN Rate", width=10, justify="right")
    table.add_column("FP Rate", width=10, justify="right")
    table.add_column("Separation", width=12, justify="right")
    table.add_column("Avg ms", width=8, justify="right")

    # Uncanny row
    acc_color = "green" if report.accuracy >= 0.8 else "yellow"
    table.add_row(
        "[cyan]uncanny[/]",
        f"[{acc_color}]{_pct(report.accuracy)}[/]",
        _pct(report.true_positive_rate),
        _pct(report.true_negative_rate),
        _pct(report.false_positive_rate),
        f"{report.separation:.2f}",
        f"{report.avg_ms_per_sample:.1f}",
    )

    # Competitor rows
    for c in competitors:
        acc_color = "green" if c.accuracy >= 0.8 else "yellow" if c.accuracy >= 0.6 else "red"
        name = c.name
        if name == "random_baseline":
            name = "random (baseline)"

        table.add_row(
            name,
            f"[{acc_color}]{_pct(c.accuracy)}[/]",
            _pct(c.true_positive_rate),
            _pct(c.true_negative_rate),
            _pct(c.false_positive_rate),
            f"{c.separation:.2f}",
            f"{c.avg_ms_per_sample:.1f}",
        )

    console.print(table)
    console.print()

    # Winner summary
    all_accs = [(report.accuracy, "uncanny")] + [(c.accuracy, c.name) for c in competitors]
    best = max(all_accs, key=lambda x: x[0])
    if best[1] == "uncanny":
        console.print(f"  [green bold]uncanny wins[/] with {_pct(best[0])} accuracy")
    else:
        console.print(f"  [yellow]{best[1]}[/] leads with {_pct(best[0])} accuracy")
        ours = report.accuracy
        console.print(f"  uncanny: {_pct(ours)} (gap: {_pct(best[0] - ours)})")
    console.print()

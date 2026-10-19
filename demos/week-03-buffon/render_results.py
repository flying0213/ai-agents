"""Read the actual simulation CSV and create report artifacts."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    root = Path.cwd()
    with (root / "results.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("results.csv contains no experiments")
    table = [
        r"\begin{tabular}{rrrrr}",
        r"\hline",
        r"Seed & $N$ & Crossings & $\widehat{\pi}$ & $|\widehat{\pi}-\pi|$ \\",
        r"\hline",
    ]
    for row in rows:
        estimate = float(row["pi_estimate"])
        table.append(f"{int(row['seed'])} & {int(row['n'])} & {int(row['crossings'])} & {estimate:.6f} & {abs(estimate - math.pi):.6f} " + r"\\")
    table.extend([r"\hline", r"\end{tabular}"])
    (root / "results-table.tex").write_text("\n".join(table) + "\n", encoding="utf-8")
    # A plain paragraph can be directly input by the starter template.
    seeds = ", ".join(str(value) for value in sorted({int(row["seed"]) for row in rows}))
    sizes = ", ".join(str(int(row["n"])) for row in rows)
    lengths = ", ".join(sorted({row["needle_length"] for row in rows}))
    spacings = ", ".join(sorted({row["line_spacing"] for row in rows}))
    params = f"本次实际参数：seed = {seeds}；$N$ = {sizes}；针长 = {lengths}；平行线间距 = {spacings}。\n"
    (root / "results-params.tex").write_text(params, encoding="utf-8")
    fig, ax = plt.subplots(figsize=(6.8, 3.5), constrained_layout=True)
    ns = [int(row["n"]) for row in rows]
    estimates = [float(row["pi_estimate"]) for row in rows]
    ax.plot(ns, estimates, marker="o", label="Buffon estimate")
    ax.axhline(math.pi, color="black", linestyle="--", label="pi")
    ax.set_xscale("log")
    ax.set_xlabel("Number of needles (N)")
    ax.set_ylabel("Estimated pi")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.savefig(root / "results.png", dpi=180)
    plt.close(fig)
    print("wrote results-table.tex, results-params.tex and results.png")


if __name__ == "__main__":
    main()

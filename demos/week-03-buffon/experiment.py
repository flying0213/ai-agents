"""Runnable classroom example: a batch Buffon needle simulation."""

from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path

FIELDS = ("seed", "n", "crossings", "pi_estimate", "needle_length", "line_spacing")


def _geometry(length: float, spacing: float) -> None:
    if not math.isfinite(length) or not math.isfinite(spacing):
        raise ValueError("length and spacing must be finite")
    if not 0 < length <= spacing:
        raise ValueError("require 0 < length <= spacing")


def crosses_line(distance: float, angle: float, length: float = 0.5, spacing: float = 1.0) -> bool:
    """Touching a line counts as crossing; angle is relative to the line."""
    _geometry(length, spacing)
    if not math.isfinite(distance) or not 0 <= distance <= spacing / 2:
        raise ValueError("distance must be in [0, spacing / 2]")
    if not math.isfinite(angle) or not 0 <= angle <= math.pi / 2:
        raise ValueError("angle must be in [0, pi / 2]")
    return distance <= length / 2 * math.sin(angle)


def estimate_pi(n: int, crossings: int, length: float = 0.5, spacing: float = 1.0) -> float:
    _geometry(length, spacing)
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    if isinstance(crossings, bool) or not isinstance(crossings, int) or not 0 < crossings <= n:
        raise ValueError("crossings must be a positive integer no larger than n")
    return 2 * length * n / (spacing * crossings)


def simulate(n: int, seed: int = 42, length: float = 0.5, spacing: float = 1.0) -> dict:
    _geometry(length, spacing)
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    rng = random.Random(seed)
    crossings = 0
    for _ in range(n):
        distance = rng.uniform(0.0, spacing / 2)
        angle = rng.uniform(0.0, math.pi / 2)
        crossings += crosses_line(distance, angle, length, spacing)
    return {
        "seed": seed,
        "n": n,
        "crossings": crossings,
        "pi_estimate": estimate_pi(n, crossings, length, spacing),
        "needle_length": length,
        "line_spacing": spacing,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Buffon needle simulation")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n", type=int, nargs="+", default=[1000, 10000, 100000])
    parser.add_argument("--length", type=float, default=0.5)
    parser.add_argument("--spacing", type=float, default=1.0)
    args = parser.parse_args()
    output = Path.cwd() / "results.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for n in args.n:
            row = simulate(n, args.seed, args.length, args.spacing)
            writer.writerow(row)
            print(f"seed={args.seed}, n={n}, crossings={row['crossings']}, pi={row['pi_estimate']:.8f}")
    print(f"wrote {output.name}")


if __name__ == "__main__":
    main()

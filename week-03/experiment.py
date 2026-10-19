"""蒲丰投针实验：真实取样，输出结果到 results.csv。

只依赖标准库；matplotlib/pytest 是项目依赖但本文件不使用。
import 本模块不会启动实验，也不会写文件。
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path

DEFAULT_LENGTH = 0.5
DEFAULT_SPACING = 1.0
DEFAULT_SEED = 42
DEFAULT_SIZES = (1000, 10000, 100000)

FIELDS = (
    "seed",
    "n",
    "crossings",
    "pi_estimate",
    "needle_length",
    "line_spacing",
)

CSV_NAME = "results.csv"


def _validate_geometry(length: float, spacing: float) -> None:
    """校验针长与线间距的关系，非法时抛出 ValueError。"""
    if spacing <= 0:
        raise ValueError(f"线间距 spacing 必须为正数，收到 {spacing!r}")
    if length <= 0:
        raise ValueError(f"针长 length 必须为正数，收到 {length!r}")
    if length > spacing:
        raise ValueError(
            f"针长 length 不能大于线间距 spacing（{length!r} > {spacing!r}）"
        )


def crosses_line(
    distance: float,
    angle: float,
    length: float = DEFAULT_LENGTH,
    spacing: float = DEFAULT_SPACING,
) -> bool:
    """判断一根针是否与平行线相交。

    坐标约定：distance 为针心到最近一条线的距离，取值 [0, spacing/2]；
    angle 为针与平行线的夹角，取值 [0, pi/2]。二者独立均匀取样。
    相交判据：distance <= (length / 2) * sin(angle)，接触也算相交。
    不合法的几何参数抛 ValueError，不静默修正。
    """
    _validate_geometry(length, spacing)

    if not 0 <= distance <= spacing / 2:
        raise ValueError(
            f"distance 必须落在 [0, {spacing / 2}]，收到 {distance!r}"
        )
    if not 0 <= angle <= math.pi / 2:
        raise ValueError(
            f"angle 必须落在 [0, {math.pi / 2}]，收到 {angle!r}"
        )

    threshold = (length / 2) * math.sin(angle)
    return bool(distance <= threshold)


def estimate_pi(
    n: int,
    crossings: int,
    length: float = DEFAULT_LENGTH,
    spacing: float = DEFAULT_SPACING,
) -> float:
    """用相交比例估计圆周率：2 * length * n / (spacing * crossings)。

    n 为正整数；crossings 为整数且 0 <= crossings <= n。
    crossings = 0 时该式无法估计，抛 ValueError。
    """
    _validate_geometry(length, spacing)

    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError(f"n 必须为正整数，收到 {n!r}")
    if not isinstance(crossings, int) or isinstance(crossings, bool):
        raise ValueError(f"crossings 必须为整数，收到 {crossings!r}")
    if crossings < 0 or crossings > n:
        raise ValueError(
            f"crossings 必须落在 [0, {n}]，收到 {crossings!r}"
        )
    if crossings == 0:
        raise ValueError("crossings 为 0 时无法用该公式估计圆周率")

    return 2 * length * n / (spacing * crossings)


def simulate(
    n: int,
    seed: int = DEFAULT_SEED,
    length: float = DEFAULT_LENGTH,
    spacing: float = DEFAULT_SPACING,
) -> dict:
    """独立跑一次投针实验，返回本次结果的字典。

    在循环外用 seed 初始化随机数生成器一次，循环内持续取样；
    不会在每次投针时重设 seed。
    """
    _validate_geometry(length, spacing)
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError(f"n 必须为正整数，收到 {n!r}")

    rng = random.Random(seed)  # 只在循环外初始化一次
    half_spacing = spacing / 2
    half_length = length / 2

    crossings = 0
    for _ in range(n):
        distance = rng.uniform(0.0, half_spacing)
        angle = rng.uniform(0.0, math.pi / 2)
        if distance <= half_length * math.sin(angle):
            crossings += 1

    if crossings == 0:
        raise RuntimeError(
            f"本次 n={n}（seed={seed}）没有任何相交，无法估计圆周率"
        )

    return {
        "seed": seed,
        "n": n,
        "crossings": crossings,
        "pi_estimate": estimate_pi(n, crossings, length=length, spacing=spacing),
        "needle_length": length,
        "line_spacing": spacing,
    }


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="蒲丰投针实验")
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"随机数种子（默认 {DEFAULT_SEED}）",
    )
    parser.add_argument(
        "--n",
        type=int,
        action="append",
        dest="sizes",
        help="投针数，可重复指定；省略时使用默认三组",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    sizes = tuple(args.sizes) if args.sizes else DEFAULT_SIZES
    seed = args.seed

    rows = []
    for n in sizes:
        # 每组独立实验开始时初始化一次随机数生成器。
        result = simulate(n, seed=seed)
        rows.append(result)
        print(
            f"[n={n:>7}] 相交 {result['crossings']:>6} 次，"
            f"估计 pi = {result['pi_estimate']:.6f}"
        )

    out_path = Path.cwd() / CSV_NAME
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"已写入 {out_path}（seed={seed}，共 {len(rows)} 组）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

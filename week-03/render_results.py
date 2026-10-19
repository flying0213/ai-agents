"""由真实 results.csv 生成报告所需片段：表格、图像与参数说明。

只读取当前工作目录的 results.csv，不重新投针、不编造结果。
输出：results-table.tex、results.png、results-params.tex。
图片坐标轴使用英文，避免额外的中文字体安装任务。
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 无需交互式后端，便于脚本运行
import matplotlib.pyplot as plt

CSV_NAME = "results.csv"


def read_results(path: Path) -> list[dict]:
    """读取并校验 results.csv，返回按 n 升序排列的行。"""
    if not path.is_file():
        raise FileNotFoundError(
            f"找不到 {path.name}。请先运行 experiment.py 生成真实结果。"
        )

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if not rows:
        raise ValueError(f"{path.name} 没有数据行，无法生成报告片段。")

    parsed = []
    for row in rows:
        parsed.append(
            {
                "seed": int(row["seed"]),
                "n": int(row["n"]),
                "crossings": int(row["crossings"]),
                "pi_estimate": float(row["pi_estimate"]),
                "needle_length": float(row["needle_length"]),
                "line_spacing": float(row["line_spacing"]),
            }
        )
    parsed.sort(key=lambda item: item["n"])
    return parsed


def _format_number(value: float) -> str:
    """把数字排成适合 LaTeX 表格的紧凑形式。"""
    return f"{value:.6g}"


def write_table(rows: list[dict], path: Path) -> None:
    """生成可直接 input 的 booktabs 表格。"""
    lines = [
        r"\begin{tabular}{rrr}",
        r"\toprule",
        r"投针数 $N$ & 相交数 $K$ & 估计值 $\widehat{\pi}$ \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{row['n']} & {row['crossings']} & "
            f"{row['pi_estimate']:.6f} \\\\"
        )
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_params(rows: list[dict], path: Path) -> None:
    """生成短的参数说明文字，内容来自 CSV 实际值。"""
    seeds = sorted({row["seed"] for row in rows})
    sizes = [row["n"] for row in rows]
    lengths = sorted({row["needle_length"] for row in rows})
    spacings = sorted({row["line_spacing"] for row in rows})

    seed_text = "、".join(str(value) for value in seeds)
    sizes_text = "、".join(str(value) for value in sizes)
    length_text = "、".join(_format_number(value) for value in lengths)
    spacing_text = "、".join(_format_number(value) for value in spacings)

    text = (
        f"本次实验使用随机种子 seed = {seed_text}，"
        f"针长 $L = {length_text}$，线间距 $d = {spacing_text}$，"
        f"投针数 $N$ 为 {sizes_text}。"
    )
    path.write_text(text + "\n", encoding="utf-8")


def write_figure(rows: list[dict], path: Path) -> None:
    """画一张静态图：不同 n 对应的估计值与真实 pi 参考线。"""
    sizes = [row["n"] for row in rows]
    estimates = [row["pi_estimate"] for row in rows]

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=150)
    ax.axhline(
        math.pi,
        color="crimson",
        linestyle="--",
        linewidth=1.2,
        label=r"true $\pi$",
    )
    ax.plot(
        sizes,
        estimates,
        marker="o",
        color="navy",
        linewidth=1.6,
        label="Buffon estimate",
    )
    for x, y in zip(sizes, estimates):
        ax.annotate(f"{y:.4f}", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8)

    ax.set_xscale("log")
    ax.set_xlabel("number of throws n (log scale)")
    ax.set_ylabel(r"estimated $\pi$")
    ax.set_title("Buffon needle: pi estimate vs. number of throws")
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="由当前目录的 results.csv 生成报告片段，不重新投针。"
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path.cwd() / CSV_NAME,
        help=f"输入 CSV（默认 {CSV_NAME}）",
    )
    args = parser.parse_args()

    rows = read_results(args.csv)
    out_dir = args.csv.parent

    write_table(rows, out_dir / "results-table.tex")
    write_params(rows, out_dir / "results-params.tex")
    write_figure(rows, out_dir / "results.png")

    print(
        f"已由 {args.csv.name} 生成 results-table.tex、results-params.tex、"
        f"results.png（共 {len(rows)} 组）"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

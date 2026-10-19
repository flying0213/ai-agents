#!/usr/bin/env bash
# 固定运行入口：算法在 Python 中；本脚本只串联已有程序。
# 不运行 pytest。公开测试请单独执行 uv run --locked pytest -q。
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_dir"
stage="检查运行环境"
trap 'code=$?; printf "\n失败阶段：%s（退出码 %s）。先检查上面的报错，再重试。\n" "$stage" "$code" >&2; exit "$code"' ERR

if ! command -v uv >/dev/null 2>&1; then
  printf '找不到 uv。请先按 Guide 安装 uv，并重新打开终端。\n' >&2
  exit 1
fi
if command -v latexmk >/dev/null 2>&1; then
  tex_engine="latexmk"
elif command -v xelatex >/dev/null 2>&1; then
  tex_engine="xelatex"
else
  printf '找不到 LaTeX 编译引擎。LaTeX Workshop 扩展不能替代 TeX Live；请先按 Guide 安装。\n' >&2
  exit 1
fi

stage="运行投针实验"
printf '\n[1/3] %s\n' "$stage"
uv run --locked python experiment.py "$@"

stage="由实际 CSV 生成图表与参数"
printf '\n[2/3] %s\n' "$stage"
uv run --locked python render_results.py

stage="编译 LaTeX 报告"
printf '\n[3/3] %s\n' "$stage"
if [[ "$tex_engine" == "latexmk" ]]; then
  latexmk -xelatex -interaction=nonstopmode -halt-on-error report.tex
else
  # 两遍处理交叉引用；这只是已安装 XeLaTeX 时的简便后备路线。
  xelatex -interaction=nonstopmode -halt-on-error report.tex
  xelatex -interaction=nonstopmode -halt-on-error report.tex
fi

printf '\n重建完成：report.pdf。请打开它，核对实际参数、表格和图像。\n'

# W3 教师演示｜蒲丰投针与实验报告

这是一份可运行的参考项目，供课堂演示，也可以在本地复现。
它做**批量模拟和静态图表**，不包含动态投针动画。学生任务仍在 [`../../week-03/`](../../week-03/)；两个目录各自使用独立的 uv 项目，不互相覆盖。

## 开始运行

已经按 W2 clone 本仓库的同学，先按 W3 Guide 更新仓库，再进入演示目录；不需要另外 clone。

```bash
cd ~/course/w02-workbench/demos/week-03-buffon
uv sync --locked
```

需要已经安装 uv；项目使用 Python 3.12，`uv sync` 会按 `.python-version` 与 `uv.lock` 准备本目录的 `.venv/`。不使用 W2 根目录或学生 `week-03/` 的环境。

### 只跑 Python 实验和图表

```bash
uv run --locked python experiment.py
uv run --locked python render_results.py
```

先打开 `results.csv` 看真实结果，再打开 `results.png` 看图。图表程序还会生成 `results-table.tex` 和 `results-params.tex`，供报告使用。这两步不需要 LaTeX 编译器。

### 重建整份 PDF 报告

已按 W3 Guide 配置 XeLaTeX 后，运行：

```bash
bash rebuild.sh
```

脚本依次完成 **实验 → 图表与参数 → PDF**。运行完成后，请打开 `report.pdf` 核对。
优先使用已安装的 latexmk；没有 latexmk、但有 XeLaTeX 时会编译两遍。LaTeX Workshop 扩展不是编译器，也不是运行本脚本的前提。

### 改一组参数，再运行一次

```bash
bash rebuild.sh --seed 7 --n 1000 10000 100000 1000000
```

未安装 LaTeX 时，也可以只运行前两步：

```bash
uv run --locked python experiment.py --seed 7 --n 1000 10000 100000 1000000
uv run --locked python render_results.py
```

每次运行都会覆盖**演示目录内**对应的上一轮结果。Python 两步更新 CSV、图表和 LaTeX 输入；运行完整重建后，PDF 才会更新。默认 seed 为 42，投针数为 1000、10000、100000，针长 0.5，平行线间距 1.0。

## 文件各自做什么

- `experiment.py`：随机投针，统计相交数，计算 π 的估计值，写入 CSV。
- `render_results.py`：读取实际 CSV，生成静态图、LaTeX 表格与参数说明。
- `report.tex`：把参数、图、表放进一份中文报告；使用 TeX Live 自带字体。
- `rebuild.sh`：依次运行上述步骤；失败时停止并指出当前阶段。
- `pyproject.toml`、`uv.lock`、`.python-version`：声明并锁定本项目的 Python 环境和依赖。
- `.gitignore`：不提交本地环境、生成结果和编译中间文件。

这份实现按学生公开测试的接口编写，但不在演示目录复制一套测试。学生仍在自己的 `week-03/` 运行公开测试；演示运行成功不代替自己项目的验收。
估计值不必等于 π，样本增加也不保证每一次误差都变小。

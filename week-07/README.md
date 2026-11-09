# W7｜NumPy 数值计算调试

- `demo.ipynb` 是教师演示，均值报告和检查已经备好。演示用浏览器 Jupyter，VS Code 操作说明保留在折叠区。
- `exercises.ipynb` 是学生练习。六题围绕掩码、广播、窗口聚合、排序索引、向量试步和分组均值，各有固定数组、错误代码、函数壳和检查。建议另存一份 `exercises-my.ipynb` 再修改。

同步已有仓库中的整个 `week-07/` 目录。详细步骤见 [W7 学生指南](https://wxyinucas.github.io/teaching-hub/#/terms/2026-fall/courses/ai-agents/weeks/week-07/guide)。

## 在 VS Code 打开

从课程仓库根目录运行：

```bash
cd week-07
uv sync --locked
code .
```

打开 `exercises.ipynb`，在右上角选择本目录 `.venv` 的 Python 3.12 kernel。NumPy 已写入本周依赖，运行 `uv sync --locked` 即可安装。先读 Notebook 中的数组起步说明。VS Code 需要 Python 和 Jupyter 扩展。使用 WSL 时，从 WSL 的终端打开项目并选择 WSL 中的 `.venv`。

从旧版继续时，先保存试跑副本，再打开更新后的 Notebook 并重启 kernel。新版缺失值用 `np.nan`，检查会核对数值和数组形状。

1. 先正常运行输入格和错误示例，记录实际输出。
2. 点击要检查的代码行左侧，设置断点。从运行按钮旁的菜单选择 **Debug Cell**，停下后在 **Variables** 看当前数组、`shape` 和掩码，在 **Call Stack** 看谁调用了这个函数。
3. 改完退出调试，再正常运行原用例和另一组输入。每道检查题都要向同桌展示一次实际运行过程。

## 用浏览器运行代码格

在本周目录注册项目内核并启动 Jupyter。

```bash
uv run --locked python -m ipykernel install --sys-prefix --name ai-agents-week-07 --display-name "W7 Python 3.12"
uv run --locked jupyter notebook exercises.ipynb
```

在网页中选择 **W7 Python 3.12**。查看教师演示时打开同目录的 `demo.ipynb`，启用顶部小虫图标，通过 **View → Debugger Panel** 展开调试面板，再给代码设断点并普通运行调用格。

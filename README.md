# AI Agents｜课程工作台与每周练习

本仓库是 AI Agents 课程的学生工作台：

- W2 的 Course Check 在仓库根目录，操作说明见下文。
- W3 的蒲丰投针实验与报告材料在 [`week-03/`](week-03/)，使用说明见 [`README-materials.md`](week-03/README-materials.md)。
- 可直接运行的 W3 教师演示在 [`demos/week-03-buffon/`](demos/week-03-buffon/)，供课堂展示和本地复现，不替代学生工作目录。
- W4 的配置隔离练习在 [`week-04/`](week-04/)，含函数壳、故障对照、公开验收与 Notebook，使用说明见 [`README-materials.md`](week-04/README-materials.md)。
- W5 的数据操作与遍历材料在 [`week-05/`](week-05/)，含完整 Notebook、分段练习、三道函数任务、公开测试与 CI；使用说明见 [`README-materials.md`](week-05/README-materials.md)。

W3 沿用 W2 已经 clone 的仓库和已有 Git 历史，但在 `week-03/` 建立独立的 uv 项目。W2 根目录的代码、依赖与环境不构成 W3 的代码基线；W3 的实现、锁文件与 `.venv/` 都属于 `week-03/`。

## W2｜Course Check

这是 AI Agents 课程第二周的一次性工作台，不构成后续项目的代码基线。仓库根目录同时也是 uv 项目根目录；三节课始终在这里观察：

1. 命令在哪个目录执行；
2. 程序使用哪个项目环境；
3. 一项修改怎样出现在 Git diff 中，并被保存为本地 commit。

完整步骤以课程网站的 W2 Guide 为准。

## 恢复并运行项目

在仓库根目录执行：

```bash
uv sync --locked
COURSE_MODE=fixture uv run --locked python course_check.py
COURSE_MODE=fixture uv run --locked pytest -q
```

初始输出中的签名是：

```text
signature: teacher
```

程序报告当前事实，测试只检查已经写下的规则；测试通过不等于全部课堂任务已经完成。

## 留下公开签名

第三课时在 VS Code 中把 [`signature.toml`](signature.toml) 的教师默认值改为教师分配的公开课程代号：

```toml
[student]
signature = "s07"
```

不要写姓名、完整学号、密码、token 或其他个人信息。

随后在仓库根目录核对：

```bash
git status --short
git diff -- signature.toml
```

确认 diff 只有签名变化后，只暂存这一文件并形成一条本地提交：

```bash
git add signature.toml
git commit -m "w2: set public signature"
```

本周不执行 `git push`。commit 只保存本地历史，不会自动改变 GitHub 上的 remote。

## W3｜Agent 与实验报告

沿用已有的 `~/course/w02-workbench`。在该仓库中通过 Git 取得教师发布的材料，然后直接进入本周目录：

```bash
cd ~/course/w02-workbench
git pull --no-rebase origin main
cd week-03
code .
```

让 Agent 阅读本目录的 `README-materials.md`、`EXPERIMENT.txt`、测试与模板，在 `week-03/` 中生成独立的 `pyproject.toml`、`uv.lock` 和两个 Python 入口，再运行实验、公开测试与报告重建。

本周的 Git 提交仍属于原有仓库；不需要第二次 clone、跨目录复制材料或在 `week-03/` 中初始化新仓库。完成后按 W3 Guide 将实验报告保存到自己的 remote；本次不要求 fork 教师仓库、建立 `students/sXX/system/` 或提交 PR。配置个人 remote 后，教师材料的更新从保留的 `upstream` 获取，具体操作以 Guide 为准。

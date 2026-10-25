# AGENTS.md

## 项目是什么

通过 Gmail SMTP 定期向配置好的 Google Voice 短信网关地址发一封邮件，让 Google Voice 账号保持活跃。可以手动跑，也可以走仓库自带的月度 Actions 定时。

## 技术栈

Python，标准库。`python -m unittest discover -s tests` 跑离线测试。

## 目录

- `main.py` — 唯一入口。
- `tests/` — 离线测试。

## 本地验证

按改动选择相关离线检查，命令以仓库当前 CI 为准。先区分代码问题与环境条件，不为通过检查降低保护。

**离线测试**

```bash
python -m unittest discover -s tests
```

## 命名与文档

- 新增文档文件名小写、`-` 连接，中文版后缀 `.zh-CN.md`；`README.md`、`AGENTS.md` 等工具约定文件保留固定名称。源码沿用现有语言命名。
- 不提交审计报告、复盘、交接单、进度快照、升级计划。要追溯看 commit 历史。
- 改文件名时同一次提交改完所有引用。
- 提交前跑 `python scripts/check_hygiene.py`。

## 不要做

- 不要把 SMTP 密码、应用专用密码或收件地址写进代码或测试。全部走 secrets。
- 不要在测试里发起真实 SMTP 连接。测试只验证消息构造。

## 提交与 PR

Conventional Commits，标题中文，不超过 50 字。类型只用 `feat` `fix` `docs` `refactor` `test` `chore` `perf` `ci`。

分支名 `<type>/<主题>`，例如 `docs/normalize-filenames`。不直接推默认分支，不 force push 已 review 的分支。

提交、推送、合并及生产动作按用户已明确授权的范围执行；同范围已有授权不重复确认。

PR 描述写改了什么、为什么改、怎么验证。

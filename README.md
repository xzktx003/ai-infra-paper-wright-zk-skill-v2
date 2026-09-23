# AI Infra Paper Writer · v2

**用途：** 根据代码、配置、真实结果和推导，先还原研究逻辑，再分类、选择段落模板，生成有证据约束的中文论文初稿。

这是可安装的 Agent Skill，不是新的 LLM、自动科研平台或录用保证。它默认不运行用户仓库代码，也不启动训练。

## 从哪里读

- `SKILL.md`：智能体入口和执行顺序。CCFA 旁路只在检索、实验设计、绘图、审稿、rebuttal、投稿检查等请求命中时，读取同级的一个技能文件。
- `references/opening-sections.md`：中英文开篇的信息组织、技术细节准入和去重复检查；[六篇实例及例外](references/opening-sections-examples.md)提供正式论文来源。
- `HANDBOOK.zh-CN.md`：研究与使用手册，包含调研、路由、关系及全部模板。
- `references/existing-skills-survey.md`：14 个真实模块、6 个项目族的取舍。
- `corpus/INDEX.md`：42 篇官方录用记录及阅读级别。
- `corpus/SCOPE.md`：覆盖范围、版本与缺口，先看再使用语料。
- `templates/README.md`：7 个一级分类、20 个二级模板。
- `english-prose/`：英文主会稿的写作与审美契约（术语冻结、主语–连接、时态）及 14 条润色流程；与 `references/research-taste.md` 分开。
- `assets/launch-prompt.zh-CN.md`：可复制的启动请求。

## 安装

保持整个 `ai-infra-paper-writer/` 目录，不要只复制 SKILL.md，否则模板和语料链接会缺失。

截至 2026-09-20，官方文档支持的项目级位置如下：

**Claude Code**：`<仓库>/.claude/skills/ai-infra-paper-writer/`。[官方 Skills 文档](https://code.claude.com/docs/en/skills)

**Codex**：`<仓库>/.agents/skills/ai-infra-paper-writer/`。[官方 Skills 文档](https://developers.openai.com/codex/skills/)

例如，在目标仓库中把解压的目录复制到上述位置。已经存在同名目录时先备份或使用版本管理，不要直接覆盖。其他兼容 Agent Skills 的客户端按其本地规则安装；本版未在每个客户端实机验证。

安装后直接请求：“请使用 ai-infra-paper-writer，根据当前仓库和指定结果生成中文初稿；先做研究诊断与段落计划，不编造证据。”详见启动请求文件。

只通过聊天使用时，可上传完整包或手册，让模型按工作流执行；聊天端能否自动读取 zip 内的引用取决于其文件工具。不能自动读取时，应解压后提供需要的文件，不能假装资源已经加载。

## 工作流

```text
只读仓库/结果审计
    → 区分代码事实、观察、证明、假说
    → 建科学依赖图与资源图
    → 选择叙事类型及结构近邻
    → 主张—证据台账与缺口
    → Introduction 逐段计划 + 正文安排
    → 中文标注初稿
    → （英文主会稿）按 english-prose/ 冻结术语并审查散文
    → 逆向审查、版本交付
```

## 四个可选脚本

Python 3.10+，仅标准库。无需安装第三方包。以下 `<SKILL_DIR>` 与 `<REPO>` 替换为本地路径。

```bash
# 创建新的 papers/vN，不覆盖旧稿；返回新目录路径。
python <SKILL_DIR>/scripts/scaffold.py --repo <REPO>

# 输出只读文件/符号盘点，不执行仓库代码；out 必须是新文件。
python <SKILL_DIR>/scripts/audit_repo.py --repo <REPO> --out <NEW_PROJECT_DIR>/repo_inventory.json

# 智能体填好显式 features 后才路由。不是直接读取代码自动分类。
python <SKILL_DIR>/scripts/route_profile.py <NEW_PROJECT_DIR>/paper_profile.json

# 草稿阶段允许 proposed / 待实验标记，但不允许 verified 主张的证据类型违规。
python <SKILL_DIR>/scripts/validate_project.py --project <NEW_PROJECT_DIR> --repo <REPO>

# 外发前更严格：未核实主张与待验证标记也报错。
python <SKILL_DIR>/scripts/validate_project.py --project <NEW_PROJECT_DIR> --repo <REPO> --strict

# 运行本包的确定性契约测试。
python <SKILL_DIR>/evals/run_tests.py
```

这些脚本不调用大模型。语义诊断、文献核验、段落写作和科学审查由使用 Skill 的智能体与作者完成。脚本通过不等于论文正确。

## 研究基础与边界

42 篇经官方页面核验录用的 2025–2026 主会论文；2026-09-22 补读后，22 篇核对引言与部分正文结构，20 篇只完成摘要级分析。没有宣称全篇证明核查或结果复现。开篇专题使用六篇有目的选取的 2025 主会论文，不是会议统一写作规范。

2025 年覆盖 ICLR/ICML/NeurIPS，2026 年当前覆盖 ICLR。ICML2026 的可用列表获取存在缺口；NeurIPS2026 通知时间晚于本次研究截止日。**不是近两年所有相关论文的穷尽分析**。OPD/QAD 的官方技术博客和报告单列为补充，不冒充录用论文。

14 个写作/研究 Skill 模块来自 6 个项目族，原始链接及采用/不采用理由齐全。未运行或比较第三方 Skill 的写稿效果，未固定可变分支 commit。

## 当前验证结果

已实际运行 26 项确定性测试，结果见 `evals/test-results.json`。验证的是文件、台账、路由规则和只读行为。**尚未运行 LLM A/B 写作质量评估**，方案见 `evals/README.md`。

2.0.2 另执行了 [五个合成开篇案例的前向试用](evals/opening-smoke-2026-09-22.md)，记录实际输出与局限；不能将单次冒烟检查等同于系统性写作效果验证。

## 版权与出处

本包的中文模板、分析和脚本为本次原创整理；不捆绑第三方论文 PDF、原图或完整第三方 Skill。外部资料以原链接为准，许可归原项目；本文不代其授予许可。来源角色和阅读范围在语料与调研文档中保留。

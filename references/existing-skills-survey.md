# 现有写作 Skill 调研与取舍

核验日期：2026-09-20。这里计数的是 **14 个实际模块，来自 6 个不同项目族**，不是 14 个独立团队，更不是把转载镜像重复计数。均访问了对应原始 SKILL 文件的关键规则；没有安装执行这些第三方代码，也没有验证其写作质量宣传。main/master 未固定 commit，因此记录的是访问时状态，不承诺未来内容不变。

## 调查回答了什么

已有资源分别擅长写作流程、系统论文、文献筛选、证据批判、引用和语言编辑。对本项目最有价值的不是再写“背景—方法—实验”，而是把它们接成：**事实提取→研究诊断→叙事路由→证据约束的段落计划→起草→逆向审查**。以下“缺口”指本次所读内容未见直接覆盖，不是宣称所有版本永久没有该功能。

## S01 · Orchestra Research / ML paper writing

[原始 Skill](https://raw.githubusercontent.com/Orchestra-Research/AI-Research-SKILLs/main/20-ml-paper-writing/ml-paper-writing/SKILL.md)。阅读范围：SKILL.md 关键工作流及写作规则。

**看到的做法：** 仓库、结果、贡献、outline、稿件的顺序；论点—证据闭环。

**本 Skill 吸收：** 采用仓库事实先行及段落级规划；新增证据等级和依赖图。

**不照搬/限制：** 不照抄未经独立核实的写作统计数字、通用固定页数或以换词制造新颖性。

## S02 · Orchestra Research / Systems paper writing

[原始 Skill](https://raw.githubusercontent.com/Orchestra-Research/AI-Research-SKILLs/main/20-ml-paper-writing/systems-paper-writing/SKILL.md)。阅读范围：段落蓝图、系统章节和评价要求。

**看到的做法：** 系统约束、设计、实现、微基准和端到端评价的分工。

**本 Skill 吸收：** 形成 S1/S2/S3 模板与成本账本；系统段落单独规划。

**不照搬/限制：** 系统会篇幅分配不能原样套进 ML 主会；部署文章也不应只读微基准。

## S03 · K-Dense AI / Scientific writing

[原始 Skill](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-writing/SKILL.md)。阅读范围：证据、稿件与来源规则。

**看到的做法：** 事实、证据、引用、探索性与确认性研究的区分。

**本 Skill 吸收：** 建立 claim/evidence 台账和 draft/verified 状态。

**不照搬/限制：** 自然科学通用 IMRaD 不能代替理论、系统与算法依赖路由。

## S04 · K-Dense AI / Literature review

[原始 Skill](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/literature-review/SKILL.md)。阅读范围：范围、筛选、综合流程。

**看到的做法：** 先确定范围，再筛选、去重与综合；摘要筛查与全文阅读分开。

**本 Skill 吸收：** 本项目记录官方录用、A/B 深度、版本与覆盖缺口。

**不照搬/限制：** 不把搜索到论文当作读过全文；不强制用生成图充当研究证据。

## S05 · K-Dense AI / Peer review

[原始 Skill](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/peer-review/SKILL.md)。阅读范围：评审框架与检查项。

**看到的做法：** 系统检查贡献、设计、结果、可复现性及局限。

**本 Skill 吸收：** 形成逆向审查：每条主张向证据追溯，再给修改动作。

**不照搬/限制：** 这里只评用户授权的自有稿件；不把评审口吻当学术权威，也不预测录用率。

## S06 · K-Dense AI / Citation management

[原始 Skill](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/citation-management/SKILL.md)。阅读范围：引用检索与验证工作流。

**看到的做法：** 标识符检索、书目信息核实、去重和引用管理。

**本 Skill 吸收：** 将“文献确实存在”和“它支持该句”分成两个检查。

**不照搬/限制：** 不自动填猜测的作者、venue、DOI；arXiv 版本不自动等同会议版。

## S07 · K-Dense AI / Hypothesis generation

[原始 Skill](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/hypothesis-generation/SKILL.md)。阅读范围：假说与验证设计。

**看到的做法：** 观察、假说、机制、预测、替代解释与对照。

**本 Skill 吸收：** 补出代码不能提供的研究解释层；机制未验证时保留竞争假说。

**不照搬/限制：** 不让故事生成器把提出的假说改写为已发现事实。

## S08 · K-Dense AI / Scientific critical thinking

[原始 Skill](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-critical-thinking/SKILL.md)。阅读范围：因果与证据批判规则。

**看到的做法：** 混杂、因果、偏差、适用条件和证据质量。

**本 Skill 吸收：** 公平比较协议与最便宜可区分实验；防止只看相关性。

**不照搬/限制：** 不将其他学科的评分标准直接包装成 AI Infra 官方规范。

## S09 · K-Dense AI / Scholar evaluation

[原始 Skill](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scholar-evaluation/SKILL.md)。阅读范围：评价维度与报告方式。

**看到的做法：** 结构化研究评价与证据支持的反馈。

**本 Skill 吸收：** 输出缺口及其影响范围，不以分数代替论证。

**不照搬/限制：** 不生成接受概率，不用单一 Taste 分值把纯理论或负结果判死刑。

## S10 · K-Dense AI / Venue templates

[原始 Skill](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/venue-templates/SKILL.md)。阅读范围：会议模板与要求获取。

**看到的做法：** 按 venue、year、track 获取格式和投稿要求。

**本 Skill 吸收：** 设置 venue_profile；写稿前核对当年官方页。

**不照搬/限制：** 不预置永久有效的页数、匿名、AI 使用和 checklist 规则。

## S11 · Anthropic / Skill creator

[原始 Skill](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)。阅读范围：技能结构、迭代与评估。

**看到的做法：** 触发边界、渐进加载、scripts/references/assets、迭代评估。

**本 Skill 吸收：** 主 SKILL 保持短入口；详细模板按路由读；加入确定性测试和待执行的 LLM A/B 计划。

**不照搬/限制：** 通过语法测试不代表写作质量已经验证；不能用自选成功案例给自己打高分。

## S12 · OpenGHz / Embodied AI paper writer

[原始 Skill](https://raw.githubusercontent.com/OpenGHz/embodied-ai-paper-writer/main/SKILL.md)。阅读范围：领域写作 playbook 及路由。

**看到的做法：** 以领域论文分析形成 abstract/intro、方法、实验和图表 playbook。

**本 Skill 吸收：** 采用样本卡→模板→段落计划的结构；改为 AI Infra 的问题和资源语义。

**不照搬/限制：** 原项目的论文数量及效果属于作者描述，本次未独立复核其全部语料；不照搬具身领域故事。

## S13 · blader / Humanizer

[原始 Skill](https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md)。阅读范围：语言模式与编辑规则。

**看到的做法：** 识别空泛拔高、重复排比和机械表达。

**本 Skill 吸收：** 只在证据及逻辑锁定后作语言清理。

**不照搬/限制：** 不为“去 AI 味”删限定词、虚构经历或逃避披露；不让风格编辑改动科学结论。

## S14 · Composio / Content research writer

[原始 Skill](https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/master/content-research-writer/SKILL.md)。阅读范围：研究写作的迭代流程。

**看到的做法：** 研究、提纲、段落迭代与来源反馈。

**本 Skill 吸收：** 采用先 outline 后 prose 和局部修改流程。

**不照搬/限制：** 传播性 hook 不等于科学动机；通用内容写作不能控制量化/蒸馏/系统证据。

## 邻近工具：不混入 Skill 数量

**Sakana AI-Scientist-v2**：[官方仓库](https://github.com/SakanaAI/AI-Scientist-v2)。仓库将其描述为从想法、实验到稿件的自动研究系统，并明确提示执行模型生成代码的风险。它启发“实验管理与写作分层”，但本 Skill 不模仿其默认自主实验：写稿阶段不安装依赖、不启动训练、不使用 GPU、不上传私有代码。仓库的 workshop 结果不是三大主会写作效果证明。

**ICML 的 PAT 实验项目**：[官方说明](https://blog.icml.cc/2026/01/14/icml-experimental-program-using-googles-paper-assistant-tool-pat/)。其定位是作者可见的纠错反馈，与正式评审分开，也要求作者核验错误提示。这里借鉴“检查证明、实验设置和推理漏洞”，不声称提供同等模型能力，也不把反馈叫官方审稿。

## 与原版相比真正补上的连接

| 原有常见能力 | 仍缺的连接 | 本次落点 |
|---|---|---|
| 从代码/结果生成稿件 | 代码事实如何区别于研究解释 | evidence-contract.md、仓库审计工作流 |
| Narrative / claim-evidence | 不同叙事怎样选择段落次序 | 7 类、20 模板及 router |
| 多篇论文 playbook | 录用、原文、版本、阅读深度是否可信 | 42 篇 corpus 与 A/B 标签 |
| 一般消融建议 | 严格依赖、协同、执行先后如何区分 | relations.md |
| 系统性能汇报 | 有效 bit、教师成本、额外硬件、prefill/decode | domain-contracts.md |
| 风格优化 | 改顺语言时不能升级证据强度 | 起草与反向审查契约 |

## 来源与授权边界

此包保存的是原创中文分析、短功能概括与原始链接，没有拷贝第三方完整 Skill、论文 PDF 或图。第三方内容的许可继续由其原项目决定；未来需要复制原文或代码时另行检查许可证。未确认的许可证、commit 和测试结果一律不补写。

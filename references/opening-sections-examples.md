# 开篇写作实例：三大会六篇论文

核对日期：2026-09-22。样本为有目的选择的 2025 年 ICLR、ICML、NeurIPS 主会论文，每会两篇；不是随机样本、频率统计或录用原因研究。以下是中文结构分析，不是原文翻译或可照抄句库。

阅读限于摘要、完整 Introduction 与标明的正文部分；未逐项验证证明或复现实验。录用状态由官方出版页确认，结构判断来自下列正式 PDF。论文“这样写过”能提供实例或反例，不能证明“必须这样写”。执行规则见 [opening-sections.md](opening-sections.md)。

## P03 · QERA · ICLR 2025

[官方出版页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/21718991f6acf19a42376b5c7a8668c5-Abstract-Conference.html) · [正式 PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/21718991f6acf19a42376b5c7a8668c5-Paper-Conference.pdf)。本次阅读：PDF pp.1–3，摘要、完整引言及相关工作/方法衔接。

**实际写法：** 引言前部用量化权重加低秩项的表达建立共同重构对象，再把参数高效微调与训练后量化放入同一视角。随后区分权重近似误差与层输出误差，由目标区别导向解析求解及带统计假设的高效形式。贡献陈述含技术解释，非每项一句。

**可迁移：** OS1/OS3——先定义需要区分的对象，才让读者理解改动为何重要。

**对过严规则的反例：** 数学表达可承担引言的解释职责；不可一律删公式或把两种应用改写成两个阶段。带条件的解析结论不能为简洁改成无条件保证。

## P14 · MagicDec · ICLR 2025

[官方出版页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/13f972adf12bdf886583d48cd528002f-Abstract-Conference.html) · [正式 PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/13f972adf12bdf886583d48cd528002f-Paper-Conference.pdf)。本次阅读：PDF pp.1–3 的摘要和完整引言，以及 §3 开头。

**实际写法：** 从长上下文服务的延迟与吞吐需求进入，解释短上下文下的大批量验证开销为何使投机解码显得不利，再分步说明上下文变长后 KV 读取成为瓶颈、转变阈值依赖模型与硬件，以及压缩草稿 KV 的机会。最后引出设计和策略选择。

**可迁移：** OS1/OS3——收益条件本身可以是开篇的关键技术信息，硬件背景不只是实验设置。

**对过严规则的反例：** 较长引言、分条洞察和章节预告不自动等于啰嗦。不能只留下“长上下文可加速”，删除批量、序列长度及瓶颈条件；也不必模仿其中强调性的修辞。

## P16 · FlatQuant · ICML 2025

[官方出版页](https://proceedings.mlr.press/v267/sun25l.html) · [正式 PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/sun25l/sun25l.pdf)。本次阅读：摘要 p.1，引言 pp.1–2，Motivation pp.2–3，Method pp.3–4。此次以正式版本核对开篇，区别于旧卡引用的 arXiv v4。

**实际写法：** 分布仍不够平坦促使采用逐层可学习仿射变换；变换的执行成本又导向 Kronecker 参数化与内核融合。摘要保留这些关键操作，引言解释访存和内核启动开销。独立 Motivation 用分布及误差分析进一步支撑平坦性判断。贡献分为四项。

**可迁移：** OS1/OS2/OS4——系统实现若解释收益来源就应在开篇出现；重复主题可以通过新增分析推进论证。

**对过严规则的反例：** 不应把所有实现移出引言、删除整个 Motivation 或强行合并为三项贡献。论文有辅助步骤不意味着每一步都应单列原创贡献。

## P23 · Olica · ICML 2025

[官方出版页](https://proceedings.mlr.press/v267/he25m.html) · [正式 PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/he25m/he25m.pdf)。本次阅读：摘要 p.1，完整引言 pp.1–2，方法 pp.3–4；由原来的 A 级摘要入口补读为 B 级。

**实际写法：** 从重训练成本进入结构化剪枝；摘要直接指明作为整体处理的注意力权重乘积对象。引言进一步说明按头分解的计算好处和 FFN 线性校准，并以连续段落中的编号概括贡献。

**可迁移：** OS1/OS3/OS4——对象、操作与成本的联系比避免数学符号更重要；贡献也可以融入连续行文。

**对过严规则的反例：** 摘要可以有关键公式。其无重训练表述有重复，不能因正式录用就认定每处重复均值得模仿；无重训练也不等于无校准成本。

## P24 · EAGLE-3 · NeurIPS 2025

[官方出版页](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c7b5a35ea98b62512a869c19ea7b03cb-Abstract-Conference.html) · [正式 PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/c7b5a35ea98b62512a869c19ea7b03cb-Paper-Conference.pdf)。本次阅读：摘要、完整引言 pp.1–3 及 §3 开头 p.4。

**实际写法：** 从增加训练数据收益有限出发，讨论特征预测约束；去除约束改善首步，却暴露多步训练与推理错位，随后引出训练期模拟推理和多层特征。引言保留解释这些转折所需的特征及损失信息，贡献项允许多句。

**可迁移：** OS3——中间失败解释了下一项设计为何需要，不能删除后只剩几个技巧名。

**对过严规则的反例：** 不是每种方法都能压成“问题一→阶段一，问题二→阶段二”；链条长并不必然冗余。其机制解释也不能直接借作另一个方法的实验证据。

## P28 · Shapley-MoE · NeurIPS 2025

论文全名：Discovering Important Experts for Mixture-of-Experts Models Pruning Through a Theoretical Perspective。

[官方出版页](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c66a9db149261435664284a20b6f1d42-Abstract-Conference.html) · [正式 PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/c66a9db149261435664284a20b6f1d42-Paper-Conference.pdf)。本次阅读：摘要、完整引言 pp.1–3，以及 p.3 方法开头。

**实际写法：** 对比打分与子集搜索，转向专家共同贡献及 Shapley 视角，再解释精确计算成本、近似估计困难，以及截断和路由引导采样各自的作用。摘要保留多个有功能解释的技术操作；引言不用独立的三条贡献列表。

**可迁移：** OS1/OS3/OS4——术语应随所解决的问题进入，而非按术语数目限额删除；贡献形式可以多样。

**对过严规则的反例：** 不能强制一段只出现一个技术名或补造三项贡献。本记录分析作者的论证组织，不独立背书其全部理论与首创声明。

## 这些实例支持什么、不支持什么

- 支持按信息功能而非字数、公式数或贡献数组织开篇；机制链、条件和实现都可能必要。
- 支持区分有证据推进的再次解释与同层次换名复述，但不提供可自动执行的重复阈值。
- 不证明某种句法更易录用，不构成六篇共同认可的写作规范。OS5 的“少作者自辩”和 OS6 的证据边界来自本 Skill 的编辑与证据契约，不能伪装成样本统计结论。

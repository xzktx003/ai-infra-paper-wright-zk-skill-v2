# 样本范围、核验标准与局限

## 范围不是“全部近两年论文”

本版以 **2025–2026 年**为近两年，截止 **2026-09-20**。使用目的抽样，兼顾量化、剪枝/联合压缩、蒸馏和投机解码的不同论证结构；不是预注册系统综述，不估计模板使用频率，也不解释录用的因果因素。

当前 **42 篇主会录用记录，21 篇 B 级结构卡，21 篇 A 级摘要入口**。正文可访问性使结构样本存在偏差，尤其 ICML 2025 的结构细读仅覆盖 FlatQuant；不能将其代表整个 ICML。没有记录声称完成全文全部证明审查或实验复现。

| 年份会议 | 已核验录用 | B：引言/部分正文 | A：摘要 |
|---|---:|---:|---:|
| ICLR 2025 | 15 | 7 | 8 |
| ICLR 2026 | 13 | 9 | 4 |
| ICML 2025 | 8 | 1 | 7 |
| NeurIPS 2025 | 6 | 4 | 2 |

## 阅读等级

- **A — abstract**：确认正式发表和摘要内容；可以定位相关工作，不能作“第三段写什么”的证据。
- **B — introduction-and-selected-body**：核对引言与标注的部分正文、目录或图表；卡内记录定位、版本与可迁移的功能。**不是“通读并验证整篇论文”**。
- **C — full-paper-structure**：保留给未来逐节完整核对的记录。本版没有 C；禁止把 B 自动升级。
- **V — result/proof verification**：与 A/B/C 正交。需要独立复现或逐项证明核查；本版没有 V。

## 官方渠道与缺口

[ICLR 2025 proceedings](https://proceedings.iclr.cc/paper_files/paper/2025)、[ICLR 2026 proceedings](https://proceedings.iclr.cc/paper_files/paper/2026)、[ICML 2025 PMLR](https://proceedings.mlr.press/v267/)、[NeurIPS 2025 main-conference](https://proceedings.neurips.cc/paper_files/paper/2025/vol38-main-conference) 为录用/出版核验入口。NeurIPS 的其他 track 不自动归为主会。

**ICML 2026：存在覆盖缺口。** 本次尝试官方 virtual 列表及 OpenReview group，未取得可用的完整论文列表，因此未纳入可核验的 2026 ICML 论文样本。不是说该会议尚未举办或不存在录用论文，也不以预印本猜测其录用状态。

**NeurIPS 2026：不纳入已录用集。** [官方日期表](https://neurips.cc/Conferences/2026/Dates) 列出主会作者通知为 2026-09-24，晚于本次截止日。待通知后重新核验，不能提前填入。

有些官方 PDF 过大、超时或以不可读取的附件格式返回。遇到这种情况，保留 A 标签；可读取作者 arXiv HTML 时，将录用验证和结构来源分开。FlatQuant 使用 v4（2025-08-10），QERA、Quamba 使用访问时未固定 revision 的 HTML。原文结构可能与 camera-ready 不完全一致。

## 对 OPD 与 QAD 的处理

它们是研究/训练设定，不是叙事类型。SKD、BOND、TAID、推理 QAT 等录用论文进入主样本；术语与最近实践补充如下，两者**不计入 42 篇录用论文**：

- [Thinking Machines — On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/)：学生轨迹与教师反馈的实践说明。
- [NVIDIA — Nemotron QAD](https://research.nvidia.com/labs/nemotron/nemotron-qad/)：量化学生与教师蒸馏的技术说明。

OPD 的轨迹来源、蒸馏损失方向、QAD 的量化位置是不同轴；不能把 reverse KL、OPD、QAD 当同义词。主张应追溯到具体实现及原文，而不是术语印象。

## 可复核检索过程与扩展协议

本次实际路径是：官方论文索引→按领域定位→官方摘要确认→官方 PDF/作者 HTML→引言和关键正文→功能编码。已有 skill 通过原始 GitHub SKILL 文件核对。没有保存可重放的完整搜索引擎结果快照，故不宣称“检索召回率”或“没有漏文”。

扩展时必须保留：访问日期、原始 URL、venue/year/track、录用证据、全文来源及版本、读到哪里、失败访问原因、叙事解释。相同论文多版本按同一记录管理；不能用标题相似就合并，也不能按摘要补造章节。

模板由 B 级样本和明确标注的结构设计共同产生。P1 新问题模板、纯理论中的无实验变体等覆盖仍偏少；它们是有条件的通用设计，不宣称从多篇本期录用论文统计得到。稿件采用模板前仍应读至少两篇结构近邻，若库内不足则检索补读。

# 英文稿写作层（ICLR 类主会散文）

本目录是 **AI Infra 英文稿的写作与审美契约**，与 `references/research-taste.md` 分开。

| 层 | 文件 | 管什么 | 不管什么 |
|---|---|---|---|
| 研究品味 | `references/research-taste.md` | 现象、机制、公平比较、资源墙、主张强度 | 主语、时态、术语换名、句尾焦点 |
| 证据契约 | `references/evidence-contract.md` | 代码/实测/证明/文献能否支撑某句 | 句子好不好读 |
| 英文散文 | **本目录** | 术语冻结、主语–连接关系、时态、段落推进、中式腔、信息焦点 | 录用概率、官方页数、是否该做实验 |

**不是 ICLR 官方要求。** ICLR 硬约束仍是当年征稿页的篇幅、匿名、Reproducibility / Ethics / AI Use 与模板。本目录只约束「读起来像主会英文论证」，不能用文采覆盖证据缺口。

## 何时加载

在 `draft` / `revise` 且目标稿是 **英文主会**（ICLR / ICML / NeurIPS 或同等匿名 PDF）时加载。纯中文初稿、只做 `diagnose` / `outline` 时不要整目录塞进上下文。

按需读，不要一次读完：

1. 本 `README.md`（何时用、与研究品味的边界）
2. 用户要润色英文、过 ICLR/ICML/NeurIPS 文风时：`polish-workflow.md`（检查簇的执行顺序）
3. `prose-contract.md`（可执行规则与例外）
4. 需要钉术语时再读 `glossary.md`
5. 换连接词或动词时读 `connectives.md`；按章节改口吻时读 `section-voice.md`
6. 讨论 14 条是否过严/不够时读 `rule-coverage.md`（分析文档，不是每轮必读）
7. 写后审查时，`workflows/review.md` 的 Pass 6 按簇执行，不要 14 路并行

## 与中文工作流的关系

中文初稿仍按 `SKILL.md` 的证据链写。英译或直接写英文时：

- 先冻结 `glossary.md` 里的名词，再写句子。
- 主张强度仍由 `evidence-contract.md` 决定；为流畅删掉限定条件是违规。
- 方法节允许以定义或公式起句，不强制每段主题句。

## 一句话原则

**名词冻结，谓词和连接词变化。** 新概念首次出现必须定义；之后不得用近义名词轮换。动词、形容词、连接词应当多样，以免同一关联词反复出现。

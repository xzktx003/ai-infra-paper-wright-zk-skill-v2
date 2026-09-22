# 章节口吻（ICLR / ICML / NeurIPS 英文稿）

同一套 14 条，在不同节的执行强度不同。不要把引言的主题句规则打进证明。

摘要、引言和 Motivation 同时遵守 [开篇信息组织契约](../references/opening-sections.md)。下列结构建议不能覆盖关键技术区别、收益条件和证据边界。

## Abstract

- 可按场景 → 具体困难 → 方法机制（用已冻结名词）→ 条件性证据组织；不是固定句数，也不强制每篇都有耦合困难。
- 允许高密度；名称不能替代操作解释。必要公式、多个有明确职责的技术名可以保留，避免重复展开全称。
- 数字必须带模型或协议；不要摘要里写 `consistently SOTA`。
- 主语优先保持话题连续；不按 `We` 次数决定质量。

## Introduction

- 论证段应有可辨认的中心和推进关系，主题句位置服从推理，不强制每段首尾明示。
- 段间可按问题 → 为何旧路线不够 → 方法原则 → 证据预告推进；现象、耦合和独立贡献列表按实际研究需要设置。
- 贡献列表可用平行 `We ...`；列表外不要再目录腔。
- 新词（stall、joint selection、shared scale）必须在首次论证段定义，不要拖到方法节才解释却已在引言使用。

## Related Work

- 每一段最后一句必须回到本文对象（对比，不是点名清单）。
- 前人术语可保留，但要映射：`trellis coding (high-dimensional structured quantization, unlike our low-dimensional codewords)`。
- 少用 `however` 连开三句；改用 `unlike` / `in contrast` / `instead`。

## Preliminaries / Method

- 允许 `Let` / `Define` / `Substituting` 起句（P06 例外）。
- 相邻句必须是推导关系，不能把中文注释一句句英译成孤立陈述。
- 符号一旦定下不要换字母讲同一量。
- 图注里的词必须与正文 canonical 一致；若图用了 `majorizer`，正文首次写 `tangent separable upper bound (majorizer)`，之后只用 upper bound。

## Experiments

- 协议句：现在时 `We evaluate` / `The main setting uses`。
- 一次性操作：过去时 `Calibration used` / `models were quantized`。
- 表中观察：现在时 `Table 1 reports` / `\method{} attains`。
- 解释段必须有主题句：这段是在比表示还是在比优化。
- 例外与失败要留在句核，不要甩到句尾当附属语。

## Conclusion

- 短；重述冻结后的对象与条件性证据。
- 不要在结论里发明引言没用过的新名词。
- 不要用结论凑页。

## 中式腔对照

| 中文提纲腔 | 不要直译 | 主会写法 |
|---|---|---|
| 前者…后者… | `The former... The latter...` 连用 | 用对象名：`The surrogate... Interval search then...` |
| 首先/其次/最后 | `Firstly, Secondly, Finally` | 靠段功能推进，不用序数 |
| 本文研究了 A，提出了 B | `This paper studies A. We propose B.` | 一句里完成对象+困难，下一句给方法 |
| 也就是说 / 即 | `that is` / `namely` 后接第三个英文名 | 只保留 canonical |
| 取得了显著提升 | `significantly improves` | 写带范围的数字 |

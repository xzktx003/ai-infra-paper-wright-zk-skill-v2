# 英文术语冻结表

写英文稿或中译英之前填写。一篇论文一张表；不要把本文件里的示例当成所有 AI Infra 论文的固定词表。

## 用法

- `canonical`：正文唯一名词（或唯一名词短语）。
- `first_use`：首次出现时必须带的定义或限定。
- `forbidden_aliases`：后文不得用来指同一对象。
- 引用前人时，可出现其原词，但须立刻映射：`QTIP's trellis coding (a high-dimensional structured code, not our base codeword)`。

## 字段模板

复制到项目的 `papers/vN/glossary.md` 或 `paper_profile.json` 的 `glossary` 数组：

```text
| concept_zh | canonical | first_use | forbidden_aliases |
```

## 示例：共享尺度联合码字选择（仅示例）

| concept_zh | canonical | first_use | forbidden_aliases |
|---|---|---|---|
| 方法名 | CoS-VQ (`\method{}`) | Cooperative Shared-scale Vector Quantization | 不要再用 Vector-GSQ 当正文主名 |
| 共享尺度 | shared scale | one scale shared by all positions in a group | common scale, joint scale |
| 组尺度（存储对象） | group scale | the stored FP16 scale of a scale group | 与 shared scale 混用前必须说明是否同一对象 |
| 跨位置选码字 | joint selection | selecting several codewords together under one shared scale | joint decisions, joint optimization, combinatorial solving（后两者若出现，须标明是同一操作的不同阶段，而不是新模块） |
| 联合搜索（算法） | interval solver / joint search | the lower-envelope procedure that updates indices and the shared scale | 不要与 joint selection 轮换当两个贡献 |
| 逐点停滞 | coordinate-wise stall | no single-index update reduces the error even after scale re-optimization | combinatorial stall, plateau（图中可写 plateau，正文指回 stall） |
| 低维码字 | low-dimensional codeword | explicit codebook vector of dimension $d$ | sub-block（仅当确指 trellis/格的子块） |
| 位置 | position | a $d$-dimensional block that takes one codeword | vector, token, channel（除非真是那些对象） |
| 候选池 | candidate pool | union of shortlists at probe scales | shortlist（shortlist 只表示单探针名单） |
| 相切可分离上界 | tangent separable upper bound | $Q(\cdot\mid z_0)$ with $D\succeq H$ | majorizer（可在首次括号：upper bound (tangent majorizer)） |
| 下包络 | lower envelope | pointwise minimum of candidate lines on $s>0$ | convex hull（除非真在讲凸包） |
| 代表区间 | representative interval | open interval on which the joint combination is constant | segment, bin |
| 硬索引 | hard index | stored discrete codeword index, not a relaxation | assignment（assignment 可指整组硬索引，但首次要挂钩） |
| 真实验收 | true layer-output error | $F(\widehat W)=\|WX-\widehat W X\|_F^2$ | reconstruction error（若指权重欧氏误差，必须分开定义） |

## 谓词多样（不要写进 forbidden）

这些可以换，避免连用同一个：

- 下降：`reduce`, `lower`, `decrease`
- 上升：`improve`, `raise`, `increase`
- 对比：`whereas`, `in contrast`, `unlike`
- 因果：`therefore`, `accordingly`, `as a result`

指标名、数据集、模型名、符号 **不** 在此列：WikiText-2、PPL.AVG、ACC.AVG、$d$、$K$ 必须前后一致。

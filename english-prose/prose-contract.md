# 英文稿散文契约

研究截止与本 Skill 其余部分相同。本文件把「好论文读感」转成可检查规则，不计算分数，不预测录用。

冲突时的优先级：

```text
证据契约 > 术语冻结 > 连接关系与焦点 > 用词多样与文采
```

为了好读而改掉限定条件、换掉已定义名词、或把局部结果写成全局最优，一律视为违规。

实际润色按 `polish-workflow.md` 的顺序执行；连接词轮换用 `connectives.md`；各节口吻用 `section-voice.md`。本文件是规则表，不是逐步操作手册。

开篇的信息取舍同时按 [opening-sections.md](../references/opening-sections.md) 执行；主题句等语言建议不能覆盖必要的论证链、公式或证据条件。

## 0. 官方格式 vs 审美

| 来源 | 必须遵守 | 本文件是否替代 |
|---|---|---|
| 当年 ICLR/ICML/NeurIPS 征稿页 | 页数、匿名、声明、模板、AI 使用披露 | 否 |
| 本契约 | 英文论证是否连贯、术语是否稳定 | 否，且不可写成「官方要求」 |

## 1. 规则总表

| ID | 条目 | 地位 | 可执行检查 | 例外 |
|---|---|---|---|---|
| P12 | 新概念必须先定义；名词不可多样 | **硬** | 每个技术名词首次出现：定义 + 唯一英文；后文只准这一个 | 符号与全称并存（`\method{}` / CoS-VQ）不算换名 |
| P09 | 前后术语统一 | 并入 P12 | 对照 `glossary.md`；禁止列表中的近义不得出现 | 引用前人原文时保留其用词，并立即映射到本文术语 |
| P01 | 不要无故更换主语 | 审查 | 连续句主语变化时，新主语必须承接旧对象或旧主张 | 对比句可换到 baseline / 现象 / 定理 |
| P02 | 换主语必须有对应关系词 | 审查 | 因果 / 递进 / 转折 / 对比 必须写明，不能只靠句号 | 同一主语的平行步骤可用分号或 `and` |
| P07 | 段间要有逻辑过渡 | 审查 | 下一段首句应回指上一段的问题、限制或结果 | 新 `\section` / `\subsection` 可用定义起句 |
| P10 | 同一关联词不要连用 | 审查 | 相邻句避免连续 `therefore` / `while` / `however`；换同义 | 公式推导中的 `hence` / `thus` 可密，但论证段不行 |
| P06 | 论证段应有可辨认的中心 | **软** | 引言、相关工作、讨论：能说出本段功能；主题句可帮助显明 | 不强制首尾位置；方法/预备知识/证明允许公式或定义起句 |
| P05 | 时态符合学术惯例 | **软** | 一般事实、方法、定理用现在时；已完成的具体实验步骤用过去时 | 过去完成时仅用于「在 X 之前已经 Y」；不要为了清单而硬用 |
| P11 | 避免中式提纲腔 | **软** | 不写「前者/后者」堆砌、不连续 `This paper studies... We propose... We then...` 当目录 | 贡献列表的平行 `We ...` 可以保留 |
| P03 | 用词符合学术论文 | **软** | 口语营销词改为中性动词（`buy accuracy` → `improve accuracy`） | 已定义的工作名、数据集名保持原样 |
| P14 | 句核突出，次要状语不要甩尾 | 审查（并入 P16） | 重点（对象、动作、结果）放在主句；次要条件收进从句或前置 | 数字、引用、表号放句尾是合法的 |
| P15 | 指示代词有唯一先行词 | **审查** | `this/these/it/which` 能替换成一个已出现的名词 | 公式后的 `this` 若紧贴刚定义的量，可以 |
| P16 | 已知先于新信息；一句一个句核 | **审查** | 范围/旧对象靠前，新主张在句核；不要把定义、结果、例外挤进一句 | 摘要允许更高密度，但仍一句一个主主张 |
| P17 | 比较与表态动词带范围 | **审查** | `better/higher/improve` 必须有对象；`show/demonstrate` 仅用于已验证主张 | 相关但未隔离机制时用 `suggest/indicate` |
| P13 | 同义动词/形容词要多样 | **受限** | 只多样动词、形容词、连接词；同一段第三次才换 | **名词、方法名、符号、数据集、指标名一律不多样** |
| P04 | 语法正确 | 校对 | 主谓一致、冠词、可数/不可数、关系从句；中文作者优先查冠词 | 不上升为研究品味 |
| P08 | 所有格正确 | 校对（并入 P04） | `'s` 用于具体所有者；复杂名词用 `of`；表/图用 `Table~\ref{}` | 固定短语如 `state of the art` 保持习惯 |

## 2. 主语与连接（P01 / P02 / P07 / P10）

换主语前先问：新主语是旧对象的属性、后果、对照，还是全新话题？

| 关系 | 典型连接 | 近义替换（防连用） | 不该用的时候 |
|---|---|---|---|
| 因果 | `because`, `so`, `therefore` | `accordingly`, `as a result`, `hence` | 两句只是并列事实 |
| 递进 | `further`, `in addition` | `moreover`, `this also` | 后句其实在转折 |
| 转折 | `however`, `yet` | `nevertheless`, `still` | 后句只是补充同一方向 |
| 对比 | `whereas`, `in contrast` | `unlike`, `by comparison` | 比较对象未出现 |
| 让步 | `even after`, `although` | `even when`, `despite` | 并无让步内容 |
| 限定 | `in this setting`, `under` | `restricted to`, `for` | 把局部结果说成一般 |

坏例（换主语、无关系词）：

```text
The former uses the residual. Figure 3 shows the iteration.
```

可接受：

```text
The surrogate uses the full residual to score candidates. Figure 3 then shows how that surrogate is solved by interval search.
```

## 3. 名词冻结 vs 谓词多样（P12 / P09 / P13）

先填 `glossary.md`，再写段落。一篇论文只保留一条中心术语链。

允许：

```text
reduce / lower / decrease
improve / raise / increase
however / whereas / in contrast
```

禁止（除非 glossary 里把它们定义成不同对象）：

```text
joint selection  ↛  joint decisions / joint search / joint optimization / combinatorial solving
shared scale     ↛  common scale / group scale / joint scale
upper bound      ↛  majorizer          （若两者确为同一构造，选一个主名，另一个只在首次括号中出现）
stall            ↛  plateau / stagnation （现象只留一个主名；图注可描述曲线，但正文指回主名）
```

新概念第一次出现的句式：

```text
<Term> is <definition in one clause>. Subsequent sentences use <Term> only.
```

不要在定义前用该词，也不要用「即」「也就是」连续换三个英文名。

## 4. 时态（P05）

| 内容 | 时态 | 例子 |
|---|---|---|
| 领域事实、问题、方法机制、定理 | 现在时 | `A shared scale couples every codeword choice.` |
| 本文提出/证明（作为仍成立的主张） | 现在时 | `We construct a tangent separable upper bound.` |
| 已完成的具体实验操作 | 过去时 | `Calibration used 320 sequences.` |
| 表格中的观察（对读者仍可读） | 现在时优先 | `Table 1 reports ...` / `\method{} attains ...` |
| 过去完成时 | 少用 | 仅 `After single-index updates had converged, joint updates decreased the error.` |

同一段落不要无理由在 `We evaluate` 与 `Calibration used` 之间来回切，除非一句讲协议、一句讲已发生的操作。

## 5. 段落结构（P06 / P07）

**论证段**（Introduction、Related Work 的收束、Experiments 的解释、Conclusion）：

- 整段应能回答「本段推进了什么」；主题句可置于首尾，不强制其位置。
- 下一段用上一段留下的限制、对照或未解问题起句。

**推导段**（Preliminaries、Method、Appendix proofs）：

- 允许 `Let`, `Define`, `Substituting` 起句。
- 仍要求相邻句有推导关系（`hence`, `so that`, `this implies`），不能变成公式清单。

不要为了主题句而把方法节改成「首先 / 其次 / 最后」的中文报告体英译。

## 6. 中式腔、学术用词、句核（P11 / P03 / P14 / P15 / P16 / P17）

避免：

- 目录句：`This paper studies A. We propose B. We then do C.`
- 营销句：`mainly buy accuracy`, `a powerful framework`, `significantly novel`
- 把非重点定语单独放到句尾，使读者以为那才是主张：  
  坏：`The method remains competitive, at an actual rate of about 2 bpw, with trellis methods.`  
  较好：`At about 2 bpw, the low-dimensional codebook remains competitive with trellis methods.`

保留：

- 限定范围的状语（模型、码率、同起点）——它们是证据，不是装饰。
- 表号、引用、数字在句尾。

**P15 指代。** `This allows the solver to ...` 若前句有两个名词，必须写成 `This coupling` / `This upper bound`。`which` 紧贴其先行词，不要隔开一个从句再甩尾。

**P16 信息结构。** 读者已知的对象或范围靠前，新动作或新结果放句核：

```text
坏：The error decreases again, after the switch to joint-index updates, on three groups.
较好：After the switch to joint-index updates, the error on the three groups decreases again.
```

**P17 比较与表态。** `better` 必须能补出 `than <object> under <protocol>`。没有隔离机制时，不要把相关写成 `This shows that the stall is caused by ...`；改 `This is consistent with ...` 或 `suggests`。

按簇检查，不要 14 路并行（理由见 `rule-coverage.md`）：

1. **A 术语（P12/P09）**：名词是否首次定义且未用禁止近义？
2. **B 话题链（P01/P02/P07）**：换主语/换段是否带对的关系词？
3. **C 指代与句核（P14/P15/P16）**：`this/it/which` 能否换成唯一名词？已知是否在前？
4. **D 范围用词（P17）**：比较有对象？`show` 是否过强？
5. **E 段落与时态（P06/P05）**：论证段能否一句话复述？机制现在时、操作过去时？
6. **F–H**：中式/营销、连接词与动词仅在重复时替换、语法与冠词。he CoS-VQ's solver` 这种叠所有格

## 8. 写后检查（供 Pass 6 使用）

对每个英文段落问：

1. 本段名词是否都在 glossary 中，且未用禁止近义？
2. 主语切换是否带了表中的关系词？
3. 段功能是否可被一句话复述（推导段除外）？
4. 时态是否把「一般机制」和「已做实验」分开？
5. 有没有为文采删掉范围限定？
6. 动词/连接词是否在多样，而名词没有被多样？

输出只列原句、违反的 ID、最小改法。不给「像顶会」分数。

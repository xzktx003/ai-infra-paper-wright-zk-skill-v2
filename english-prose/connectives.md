# 连接词库（防连用，也对上关系）

相邻句不要重复同一连接词。关系选错比词重复更糟：转折句不要用 `therefore`。

## 关系 → 词

| 关系 | 首选 | 替换（相邻句用） | 典型句核 |
|---|---|---|---|
| 因果 | `because`, `so`, `therefore` | `accordingly`, `as a result`, `hence`, `for this reason` | 后句是前句的结果 |
| 递进 | `further` | `moreover`, `in addition`, `this also` | 同方向加信息 |
| 转折 | `however` | `nevertheless`, `yet`, `still` | 同方向预期被打断 |
| 对比 | `whereas` | `in contrast`, `unlike`, `by comparison` | 两个对象对打 |
| 让步 | `although`, `even after` | `even when`, `despite`, `even so` | 先承认限制再给主主张 |
| 限定 | `in this setting` | `under`, `restricted to`, `for` | 缩小主张范围 |
| 例证 | `for example` | `in particular`, `concretely` | 用数字或特例 |
| 推导 | `hence`, `so that` | `this implies`, `it follows that` | 公式/定义之后 |
| 时间顺序 | `after`, `then` | `once`, `subsequently` | 算法步骤，不是因果时不要用 `therefore` |

## 常见错配

| 原句关系 | 错用 | 改 |
|---|---|---|
| 只是并列步骤 | `therefore` | `then` / 分号 |
| 对比 baseline | `and` | `whereas` / `in contrast` |
| 让步（即使重优化尺度仍停滞） | `while` 当 although | `even after` / `although` |
| 补充同一结论 | `however` | `further` / 句内 `and` |

## 动词多样（名词不动）

| 意思 | 轮换 | 不要动的名词 |
|---|---|---|
| 下降 | `reduce`, `lower`, `decrease` | perplexity, error, PPL.AVG |
| 上升 | `improve`, `raise`, `increase` | accuracy, ACC.AVG, throughput |
| 保持 | `keep`, `retain`, `preserve` | codebook, lookup |
| 得到 | `attain`, `reach`, `obtain` | 指标名 |
| 表明 | `show`, `indicate`, `report` | Table / Figure |

同一段里同一个动词出现第三次再换。不要为了多样把 `shared scale` 写成 `common scale`。

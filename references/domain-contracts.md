# AI Infra 分方向证据与资源契约

这些检查来自问题定义及可比性要求，不是所有论文必须跑完全相同的 benchmark。依据主张选择测试，遵守用户的单 GPU 研究预算；本 Skill 默认不执行训练。

## 量化与 QAT / QAD

先记清 W/A/KV 的精度、码本/格式、group size、scale/exponent/zero-point、padding、离群/残差保护，以及是否包含 embedding/lm_head/router。名义 2 bit 不等于实际平均 2 bit；有效 bit 必须计算全部元数据与高精度残余。

区分 weight-only 存储收益、原生低精度 GEMM/GEMV、fake quant+高精度计算。PTQ 的搜索/校准成本与 QAT 的训练成本都需要记录。是否训练 weight、scale、codebook、assignment、rotation、adapter 分开写。

QAD 先填写六项：教师 checkpoint/是否冻结、学生量化位置、训练数据/轨迹来源、损失方向与归一化、教师打分/生成成本、部署是否用真实量化内核。不能因用了 distillation loss 就称 on-policy；也不能因学生有低精度格式就认定部署已实现加速。[NVIDIA 实践来源](https://research.nvidia.com/labs/nemotron/nemotron-qad/)

局部重构、PPL、零样本、生成/数学代码等证据功能不同；reasoning 模型需固定 think 模式、生成预算与采样参数。校准集不能含测试样本或先看测试结果再选最佳配置而不披露。

## 剪枝、MoE 与低秩

明确剪的是参数元素、通道、层、完整专家、微专家、激活专家还是 Token。结构化 mask 是否最终转为缩小的 dense 矩阵？仅将值设零的张量尺寸不会自动变小。

MoE 区分 **resident 参数/显存** 与 **每 token active 工作量**。完整删专家、减少 top-k、缩专家内部宽度、合并专家、跳过计算分别有不同系统后果。router 是否重归一化、是否需回退、稀有能力如何测量都要说明。

低秩写实际 factor 的两个维度和额外算子；共享与专家私有部分分开。跨专家共享可能减少容量却增加通信/访存。补偿带来的训练、参数和算子都进入预算。

专家重要性分数需要用真实移除/替代损失验证；路由频率不自动等于能力唯一性。常见领域、OOD 校准和长尾任务的覆盖按所声称机制安排。

## KD / OPD

把三个轴分别填写：**谁产生训练前缀/轨迹；谁提供监督；优化什么分布距离或奖励**。on-policy 指向学生当前策略访问的状态，不能用 loss 名称替代；off-policy 数据可来自教师、旧学生或静态数据。reverse KL 不是 OPD 定义的一部分。[实践参考](https://thinkingmachines.ai/blog/on-policy-distillation/)

记录教师/学生能力差、初始化、词表/Tokenizer兼容、温度、teacher scoring、rollout长度、缓存与序列过滤。只算学生反传省下的成本不等于总蒸馏成本降低。静态数据可被多次摊销，在线采样也要讲收益与额外成本。

若主张 train–test mismatch 被修复，不能只报最后平均分；测访问状态、错误积累、早晚训练或不同初始化的变化。理论来源是模仿学习时，应区分引用的结论与本文新证明。

## 投机解码

分清草稿生成、候选树/块、目标验证、接受/重采样、bonus token、回退与 KV 管理。记录 greedy/随机、temperature、top-p/top-k、目标分布是否精确保持、是否输出可见 token 完全一致。

接受率、平均接受长度、每轮产生 token、实际 tokens/s 不互相替代。不同草稿长度、tree宽度或批处理下接受率不可直接横比。端到端时间应包含 drafting、verification、同步、数据移动、预后处理与失败回退。

同时报告 prefill/decode、TTFT/TPOT、batch/context、并发/负载和设备数量。额外设备并行是合法收益路径，但需单独报告资源；不能用单GPU baseline和多GPU方法只比最快点。

训练草稿时区分 token拟合、feature拟合、接受率与速度目标；多步推理必须关心训练/推理状态差异。lossless 主张需要正确采样证明，不是抽几条相同文本即可。

## 纯理论、规律与基准的额外要求

理论：量词、概率保证、精确/近似、单步/多步、最坏/平均、oracle/实际计算成本不可省略。

规律：训练点、验证点、最终未见测试点明确隔离；不能把拟合后的最优点当外推能力。

基准：预注册式固定协议、数据污染检查、模型版本与代码实现公平性、完整失败/排名翻转记录。本文设计参考 P42 的问题组织，但不复制其结论到别的工作负载。

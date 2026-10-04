# Replication Guide — 一键复刻名著等文学故事写作

本指南说明如何利用三元九维 19683 坐标系的**结构指纹**生成一部保留（或镜像、变奏）原著名结构的新小说。规则细节见 [framework.md](framework.md)。

## 一、核心思想

原著 → 坐标映射 → **结构指纹**（三元重心 + 熵 + 主要转折点）→ 新故事蓝图（目标坐标序列）→ 成文 → **回贴自检**。

复刻的不是文字与情节，而是**结构**：封闭空间、人物驱动、熵值、转折频率、因果链长——这些是可计算、可对比的指纹。

## 二、三步操作

### Step 1 · 解析原著（analyze）

把原著按 [mapping-guide.md](mapping-guide.md) 落成节点坐标表，一键得出结构指纹：

```bash
tri9cog fingerprint examples/hongloumeng/mapping/nodes.csv --out fingerprint.json
```

输出示例（《红楼梦》真实指纹）：

```json
{
  "book": "hongloumeng",
  "nodes": 120,
  "unique_codes": 84,
  "code_range": [0, 18952],
  "entropy": 1.3929,
  "triad_mode": {"T": 0, "S": 0, "C": 0},
  "turning_points": [[5, 6, 8], [98, 99, 6], [116, 117, 9], [119, 120, 7]]
}
```

### Step 2 · 生成蓝图（blueprint）

选择再创作策略，输出目标坐标序列：

| 策略 | 做法 | 效果 |
| --- | --- | --- |
| 同构 (isomorphic) | 保留全部指纹 | 换壳不换骨，气质相近 |
| 镜像 (mirror) | 翻转主元（如 S3 封闭→开放、C1 人物→宿命） | 气质反转 |
| 变奏 (variation) | 保留主元、变异副元（如空间开放化） | 同源不同调 |

```bash
tri9cog blueprint --source fingerprint.json --strategy mirror --nodes 40 --out blueprint.json
```

蓝图是一组**目标节点坐标**：`{"node_1": "000-000-000", "node_2": "..."}`。

### Step 3 · 成文与自检（verify）

围绕每个目标坐标写场景、人物、冲突（人工执笔或接入大模型），然后回贴坐标系逐节点自检：

```bash
tri9cog verify new-story-nodes.csv --target blueprint.json
```

自检报告包含：逐节点偏差、指纹偏差（熵差、重心差）、转折点命中率。

## 三、案例：从《红楼梦》到《停云楼》

- 指纹来源：《红楼梦》120 回映射（见 `examples/hongloumeng/`）；
- 策略：同构（保留封闭空间 + 人物驱动 + 长链伏笔）；
- 新作：《停云楼》12 回（见 `examples/tingyunlou/tingyunlou-novel.md`），人物映射 青梧↔宝玉、清和↔黛玉、晴鸢↔晴雯；
- 做法：按蓝图坐标写场景（戏园封闭世界 = 大观园封闭世界；戏班存亡因果 = 家族兴衰因果）。

## 四、扩展建议

- **跨语言**：指纹与语言无关，可复刻任何语言的叙事结构；
- **多策略组合**：可按章节混合同构/镜像/变奏；
- **模型接入**：v0.3 将提供 LLM adapter，蓝图坐标作为硬约束喂给生成器；
- **批量复刻**：一个指纹可产出 N 部不同壳的新作，全部可通过回贴自检。
# 风格 + 结构决策模板

> 用途：歌词动笔前和 Duoqi 对齐"这歌长什么样"。
> 输入：`songs/<主题>/mood.md` 已完成（基调已定）
> 产出：`songs/<主题>/brief.md`（决策记录）+ `songs/<主题>/v1_style.txt`（Suno 风格字段）

---

## 一、歌词类型选择(从六型里挑 1-2 型)

参考 `CLAUDE.md` 六型表（叙事 / 抒情 / 哲理 / 意象 / 态度 / 功能）。

- 主型：__________（占 70%）
- 辅型：__________（占 30%，可留空）
- 为什么这么选：__________

**多版本差异化**（至少 2 版）：
- v1：主型 + 辅型 = __________
- v2：主型 + 辅型 = __________
- v3（可选）：__________

---

## 二、结构变体选择

| 变体 | 模板 | 适用 | 推荐流派 |
|---|---|---|---|
| **完整型** | V-PC-C-V-PC-C-Bridge-C | 长歌（4 分+），情绪层次多 | 抒情慢板、流行摇滚 |
| **省 PC2 型**（最常用） | V-PC-C-V-C-Bridge-C | 3-4 分钟主流 ballad | 抒情慢板、R&B、City Pop |
| **省 Bridge 型** | V-PC-C-V-PC-C-C | 紧凑、副歌洗脑 | 流行口水歌 |
| **双 V 起始** | V-V-PC-C-V-C-Bridge-C | 故事性强，需更多铺垫 | 民谣、叙事 |
| **极简型** | V-C-V-C-Bridge-C | 民谣 / 简约风 | 民谣、独立 |
| **Hook 前置** | C-V-C-V-Bridge-C | Trap / K-pop | Trap、Hip-hop |
| **功能型 / 科普** | Intro-V(密集)-Hook-V-Hook-Outro | 信息密度高 | 顺口溜、科普歌 |
| **自定义** | __________ | __________ | __________ |

**我选**：__________
**时长目标**：__________（默认 ~3 分钟）

**结构决策原则**：

- 用 PC（导歌）：V 和 C 之间能量 / 视角差距大，需要过渡
- 省 PC：想紧凑（控时长在 3 分半内）/ V 和 C 衔接已经很顺 / 第二次为了避免重复感（这就是「省 PC2」最常用的原因）
- 必须用 Bridge：歌长 ≥3 分钟 / 想给情绪"第三种颜色"（视角切换、节奏变化、突然冷下来再爆）
- Outro 写法：Hook 关键词回扫 + 升华句（不要直接重复整段副歌）

---

## 三、音乐风格（给 Suno 用）

### 3.1 主流流派速选表

每一行都是一个"开箱即用"模板。先挑 1 行为主，再去 3.2 微调。

| 流派 | 推荐结构 | Suno 友好度 | 典型配器 / 人声 | style_prompt 模板 | 适合题材 |
|---|---|---|---|---|---|
| **抒情慢板**（Mandopop ballad） | 完整型 / 省 PC2 型 | **强** | 钢琴 + 弦乐，真声拔高 | `Mandopop ballad, female vocal, piano and strings, slow 70bpm, emotional, modern production` | 情感、家人、怀旧、悲剧 |
| **City Pop** | 省 PC2 型 / 极简型 | **强** | 电钢、slap bass、暖合成器 | `city pop, mellow female vocal, warm synths, electric piano, slap bass, 1980s Tokyo, nostalgic` | 怀旧、夜晚、轻情绪 |
| **民谣 / Folk** | 双 V 起始 / 极简型 | **强** | 木吉他主导，叙事人声 | `indie folk, acoustic guitar-led, intimate male vocal, fingerpicking, storytelling, warm` | 故事、人物、历史 |
| **R&B / Soul** | 完整型 / 省 PC2 型 | **中-强** | 电钢 + 808 + 转音 | `R&B ballad, soulful female vocal, electric piano, 808 drums, smooth, late-night, ad-libs` | 暧昧、细腻、夜晚 |
| **流行摇滚** | 完整型 | **中** | 电吉他 + 鼓 + 能量 | `pop rock, powerful male vocal, distorted guitars, driving drums, anthemic, modern production` | 愤怒、宣言、热血 |
| **古风 Fusion** | 省 PC2 型 | **中-强** | 古筝 / 笛子 + 现代制作 | `chinese folk fusion, female vocal, guzheng, dizi, modern production, cinematic, poetic` | 历史、人物、意境 |
| **Trap / Hip-hop** | Hook 前置型 | **中** | 808、sub bass、auto-tune | `trap ballad, melodic male vocal, 808 drums, sub bass, atmospheric, auto-tune` | 态度、自述、年轻 |
| **轻摇滚 / Soft Rock** | 完整型 / 省 PC2 型 | **强** | 木吉他 + 电吉他 + 鼓 | `soft rock, warm male vocal, acoustic and electric guitars, mellow drums, hopeful, 90s` | 成长、回忆、平静的力量 |

**我选**：__________

> 友好度只是当前版本快照（v4.5/v5）。详细维度（语言、人声、BPM、特殊技巧）和**时效性提醒**见 `templates/ai_friendliness.md`。

### 3.2 字段微调（在速选模板的基础上改）

| 维度 | 你的选择 | 示例 |
|---|---|---|
| 流派 |  | Mandopop ballad / city pop / indie folk / trap / orchestral pop |
| 人声 |  | female vocal / male vocal / duet / 清亮 / 沙哑 / 低语 |
| 核心乐器 |  | piano-led / acoustic guitar / synths / strings |
| 节奏 |  | slow 70bpm / mid-tempo / driving 120bpm |
| 年代 / 地域感 |  | 1980s Tokyo / 90s Cantopop / modern bedroom pop |
| 情绪关键词（2-3 个） |  | nostalgic, bittersweet, defiant |

**最终 style_prompt**（写入 `v1_style.txt`，≤200 字符）：

```
（这里写最终拼好的那一行）
```

---

## 四、写作约束清单

勾选强制项，Claude 写词时不得违反：

- [ ] 中文歌词（默认）
- [ ] 英文 / 双语：__________
- [ ] **押韵**：每段至少 AABB 或 ABAB（硬要求）
- [ ] **口语化**：每句都能自然念出来，避免书面语倒装
- [ ] 避免 AI 套话：如"岁月如歌 / 心似流水 / 命运的齿轮"等
- [ ] 具象优先：抽象情感必须落到资料里的具体意象
- [ ] 副歌 hook 要短、要记得住（参考 `hook.md`）
- [ ] 敏感词 / 避雷：__________

---

## 五、参考（可留空）

- 参考歌手：__________
- 参考歌：__________（哪首的什么段落像）
- 反面参考（别像这种）：__________

---

## 六、写入 `brief.md` 的最终记录

```markdown
# <主题> · 风格 + 结构决策

- 歌词类型：v1 = <主+辅>，v2 = <主+辅>
- 结构变体：<变体名> = <段落模板>
- 时长：<X 分钟>
- 流派：<速选表选项>
- 音乐风格：<一行 style_prompt>
- 硬约束：押韵 / 口语化 / 具象 / <其他>
- 参考：<歌手 / 歌>
- 反面参考：<…>
- 决策时间：<YYYY-MM-DD>
```

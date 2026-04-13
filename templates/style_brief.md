# 风格决策模板

> 用途：歌词动笔前和 Duoqi 对齐"这歌长什么样"。
> 产出：`songs/<主题>/brief.md`（决策记录）+ `songs/<主题>/v1_style.txt`（Suno 风格字段）。

---

## 一、歌词类型选择（从六型里挑 1-2 型）

参考 `CLAUDE.md` 六型表。

- 主型：__________（占 70%）
- 辅型：__________（占 30%，可留空）
- 为什么这么选：__________

**多版本差异化**（至少 2 版）：
- v1：主型 + 辅型 = __________
- v2：主型 + 辅型 = __________
- v3（可选）：__________

---

## 二、结构选择

勾选一个，或自定义：

- [ ] **标准**：Verse1 – Chorus – Verse2 – Chorus – Bridge – Chorus
- [ ] **叙事长版**：Verse1 – Pre – Chorus – Verse2 – Pre – Chorus – Bridge – Verse3 – Chorus
- [ ] **极简**：Verse – Chorus – Verse – Chorus
- [ ] **功能型 / 科普型**：Intro – Verse(密集信息) – Hook – Verse – Hook – Outro
- [ ] 自定义：__________

时长目标：__________（2 分半 / 3 分 / 3 分半…）

---

## 三、音乐风格（给 Suno 用）

按顺序填，最后拼成一行 ≤200 字符。

| 维度 | 你的选择 | 示例 |
|---|---|---|
| 流派 |  | Mandopop ballad / city pop / indie folk / trap / orchestral pop |
| 人声 |  | female vocal / male vocal / duet / 清亮 / 沙哑 / 低语 |
| 核心乐器 |  | piano-led / acoustic guitar / synths / strings |
| 节奏 |  | slow 70bpm / mid-tempo / driving 120bpm |
| 年代 / 地域感 |  | 1980s Tokyo / 90s Cantopop / modern bedroom pop |
| 情绪关键词（2-3 个） |  | nostalgic, bittersweet, defiant |

**拼装示例**：
```
Mandopop ballad, female vocal, piano and strings, slow 70bpm, modern production, bittersweet, nostalgic
```

**最终 style_prompt**（写入 `v1_style.txt`）：
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
- [ ] 副歌 hook 要短、要记得住（8-12 字一句）
- [ ] 敏感词 / 避雷：__________

---

## 五、参考（可留空）

- 参考歌手：__________
- 参考歌：__________（哪首的什么段落像）
- 反面参考（别像这种）：__________

---

## 六、写入 `brief.md` 的最终记录

Claude 讨论完后整理成：

```markdown
# <主题> · 风格决策

- 歌词类型：v1 = <主+辅>，v2 = <主+辅>
- 结构：<结构名>
- 时长：<X 分钟>
- 音乐风格：<一行 style_prompt>
- 硬约束：押韵 / 口语化 / 具象 / <其他>
- 参考：<歌手/歌>
- 反面参考：<…>
- 决策时间：<YYYY-MM-DD>
```

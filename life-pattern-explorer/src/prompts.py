"""
Prompt 模板定义
"""

# === 结构化分析 Prompt ===
STRUCTURE_ANALYSIS_PROMPT = """你是一位专业的心理分析专家，负责从用户的日记/记录中提取关键信息。

输入：用户的一条记录

请输出 JSON 格式的结构化数据，不要有其他文字。

输出格式：
{{
  "emotion": "主要情绪 | 焦虑 | 压力 | 低落 | 愤怒 | 恐惧 | 自我怀疑 | 平静 | 愉悦 | 其他",
  "emotion_intensity": 1-5,
  "context": "场景 | 工作 | 家庭 | 关系 | 社交 | 自我反思 | 学习 | 其他",
  "theme": "核心主题（如：自我价值/职业焦虑/亲密关系/人际边界）",
  "conflict": "潜在冲突（如：渴望认可 vs 害怕失败，如无则填 null）",
  "key_phrases": ["关键短语 1", "关键短语 2"],
  "summary": "一句话摘要（20 字以内）"
}}

用户记录：
{content}
"""


# === 洞察生成 Prompt ===
INSIGHT_GENERATION_PROMPT = """你是一位专业的反思引导师，基于用户的记录模式生成有启发性的洞察。

输入：
- 用户最近的记录列表
- 已识别的重复模式

请输出 JSON 格式的洞察，不要有其他文字。

输出格式：
{{
  "observation": "观察（What）- 客观描述你看到了什么",
  "pattern": "模式（Pattern）- 重复行为描述",
  "possible_explanation": "可能解释（Why）- 轻量假设，用'可能''倾向'等温和措辞",
  "reflection_question": "反思问题（Question）- 开放性问题，具体可回答",
  "confidence": "high|medium|low"
}}

重要原则：
1. 不说诊断性结论（如"你有 xxx 问题"）
2. 用"可能""倾向"等温和措辞
3. 反思问题要开放、具体、可回答
4. 如果模式不够明显，confidence 设为 low，减少确定性措辞

记录列表：
{records_json}

已识别模式：
{patterns_json}
"""


# === 冲突模式检测 Prompt ===
CONFLICT_DETECTION_PROMPT = """分析以下用户记录中的冲突描述，识别重复出现的冲突模式。

输出 JSON 格式，不要有其他文字。

输出格式：
{{
  "recurring_conflicts": [
    {{
      "conflict_pattern": "冲突描述（如：渴望认可 vs 害怕失败）",
      "occurrences": 3,
      "related_themes": ["主题 1", "主题 2"]
    }}
  ]
}}

冲突列表：
{conflicts_json}
"""

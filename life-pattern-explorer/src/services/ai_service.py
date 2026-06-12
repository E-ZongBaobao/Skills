"""
AI 服务：LLM 调用、结构化分析、洞察生成
"""
import json
import httpx
from typing import Optional, List
from src.config import settings
from src.models.schemas import StructuredData
from src.prompts import STRUCTURE_ANALYSIS_PROMPT, INSIGHT_GENERATION_PROMPT


class AIService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.llm_model = settings.LLM_MODEL
        self.base_url = "https://openrouter.ai/api/v1"

    async def analyze_structure(self, content: str) -> StructuredData:
        """
        对记录进行结构化分析
        提取情绪、场景、主题、冲突等信息
        """
        prompt = STRUCTURE_ANALYSIS_PROMPT.format(content=content)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://life-pattern-explorer.local",
                    "X-Title": "Life Pattern Explorer",
                },
                json={
                    "model": self.llm_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 500,
                },
            )
            response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # 解析 JSON
        try:
            # 清理可能存在的 markdown 代码块标记
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            structure_data = json.loads(content)
            return StructuredData(**structure_data)
        except json.JSONDecodeError as e:
            # 如果解析失败，返回默认值
            print(f"JSON 解析失败：{e}, 原始内容：{content}")
            return StructuredData(
                emotion="其他",
                emotion_intensity=3,
                context="其他",
                theme="未分类",
                conflict=None,
                key_phrases=[],
                summary=content[:50] if len(content) > 50 else content,
            )

    async def generate_insight(
        self, records_json: str, patterns_json: str
    ) -> dict:
        """
        生成洞察报告
        """
        prompt = INSIGHT_GENERATION_PROMPT.format(
            records_json=records_json, patterns_json=patterns_json
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://life-pattern-explorer.local",
                    "X-Title": "Life Pattern Explorer",
                },
                json={
                    "model": self.llm_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5,
                    "max_tokens": 800,
                },
            )
            response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # 解析 JSON
        try:
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败：{e}, 原始内容：{content}")
            # 返回默认洞察
            return {
                "observation": "已记录你的想法，继续积累更多数据后会生成更精准的洞察。",
                "pattern": "模式分析需要更多数据支持。",
                "possible_explanation": "随着记录增多，AI 将能发现更深层的模式。",
                "reflection_question": "继续记录，给自己更多时间和空间去观察。",
                "confidence": "low",
            }


ai_service = AIService()

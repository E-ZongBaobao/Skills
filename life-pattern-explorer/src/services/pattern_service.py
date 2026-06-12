"""
模式识别服务：检测重复模式、生成洞察
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import Counter
from src.db.database import db
from src.models.schemas import Pattern, Insight
from src.services.ai_service import ai_service


class PatternService:
    def __init__(self):
        self.min_records_for_insight = 3

    async def check_trigger(self, user_id: str) -> bool:
        """
        检查是否触发模式分析
        条件：未分析记录 >= 3 条
        """
        async with db.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                SELECT COUNT(*) as count FROM records
                WHERE user_id = $1 AND analyzed = false
                """,
                user_id,
            )
            return result["count"] >= self.min_records_for_insight

    async def detect_patterns(self, user_id: str) -> List[Pattern]:
        """
        检测三种模式类型：
        1. 情绪重复模式
        2. 场景重复模式
        3. 冲突模式
        """
        async with db.pool.acquire() as conn:
            # 获取用户所有已分析记录
            records = await conn.fetch(
                """
                SELECT id, content, emotion, context, theme, raw_structure, created_at
                FROM records
                WHERE user_id = $1 AND analyzed = true
                ORDER BY created_at DESC
                LIMIT 50
                """,
                user_id,
            )

        if len(records) < 2:
            return []

        patterns = []
        now = datetime.now()

        # 1. 情绪频率统计
        emotion_counts = Counter(r["emotion"] for r in records if r["emotion"])
        for emotion, count in emotion_counts.most_common(3):
            if count >= 2:
                emotion_records = [r for r in records if r["emotion"] == emotion]
                patterns.append(
                    Pattern(
                        id=str(uuid.uuid4()),
                        type="emotion",
                        key=emotion,
                        count=count,
                        description=f"'{emotion}'情绪出现 {count} 次",
                        first_seen=emotion_records[-1]["created_at"],
                        last_seen=emotion_records[0]["created_at"],
                        sample_record_ids=[str(r["id"]) for r in emotion_records[:3]],
                    )
                )

        # 2. 场景频率统计
        context_counts = Counter(r["context"] for r in records if r["context"])
        for context, count in context_counts.most_common(3):
            if count >= 2:
                context_records = [r for r in records if r["context"] == context]
                patterns.append(
                    Pattern(
                        id=str(uuid.uuid4()),
                        type="context",
                        key=context,
                        count=count,
                        description=f"'{context}'场景出现 {count} 次",
                        first_seen=context_records[-1]["created_at"],
                        last_seen=context_records[0]["created_at"],
                        sample_record_ids=[str(r["id"]) for r in context_records[:3]],
                    )
                )

        # 3. 主题聚类
        theme_counts = Counter(r["theme"] for r in records if r["theme"])
        for theme, count in theme_counts.most_common(3):
            if count >= 2:
                theme_records = [r for r in records if r["theme"] == theme]
                patterns.append(
                    Pattern(
                        id=str(uuid.uuid4()),
                        type="theme",
                        key=theme,
                        count=count,
                        description=f"'{theme}'主题出现 {count} 次",
                        first_seen=theme_records[-1]["created_at"],
                        last_seen=theme_records[0]["created_at"],
                        sample_record_ids=[str(r["id"]) for r in theme_records[:3]],
                    )
                )

        return patterns

    async def generate_insight(self, user_id: str, patterns: List[Pattern]) -> Insight:
        """
        基于模式生成洞察
        """
        if not patterns:
            # 返回默认洞察
            return Insight(
                id=str(uuid.uuid4()),
                observation="已记录你的想法，继续积累更多数据后会生成更精准的洞察。",
                pattern="模式分析需要更多数据支持。",
                possible_explanation="随着记录增多，AI 将能发现更深层的模式。",
                reflection_question="继续记录，给自己更多时间和空间去观察。",
                confidence="low",
                related_record_ids=[],
                created_at=datetime.now(),
            )

        # 获取相关记录
        record_ids = []
        for pattern in patterns:
            record_ids.extend(pattern.sample_record_ids)

        async with db.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT id, content, created_at FROM records
                WHERE id = ANY($1)
                ORDER BY created_at DESC
                """,
                [uuid.UUID(rid) for rid in record_ids if rid],
            )

        # 准备 JSON 数据
        records_json = [
            {"id": str(r["id"]), "content": r["content"]} for r in records
        ]
        patterns_json = [
            {"type": p.type, "key": p.key, "count": p.count, "description": p.description}
            for p in patterns
        ]

        # 调用 AI 生成洞察
        insight_data = await ai_service.generate_insight(
            records_json=records_json, patterns_json=patterns_json
        )

        # 保存到数据库
        insight_id = str(uuid.uuid4())
        async with db.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO insights (id, user_id, pattern_ids, content)
                VALUES ($1, $2, $3, $4)
                """,
                insight_id,
                user_id,
                [p.id for p in patterns],
                insight_data,
            )

        return Insight(
            id=insight_id,
            **insight_data,
            related_record_ids=[str(r["id"]) for r in records],
            created_at=datetime.now(),
        )

    async def get_insights(self, user_id: str, limit: int = 10) -> List[Insight]:
        """
        获取用户的洞察历史
        """
        async with db.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, content, created_at FROM insights
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT $2
                """,
                user_id,
                limit,
            )

        insights = []
        for row in rows:
            content = row["content"]
            insights.append(
                Insight(
                    id=str(row["id"]),
                    observation=content.get("observation", ""),
                    pattern=content.get("pattern", ""),
                    possible_explanation=content.get("possible_explanation", ""),
                    reflection_question=content.get("reflection_question", ""),
                    confidence=content.get("confidence", "low"),
                    created_at=row["created_at"],
                )
            )

        return insights


pattern_service = PatternService()

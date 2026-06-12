"""
记录服务：创建记录、触发分析
"""
import uuid
from datetime import datetime
from typing import Optional
from src.db.database import db
from src.models.schemas import RecordCreate, RecordResponse, StructuredData
from src.services.ai_service import ai_service
from src.services.pattern_service import pattern_service


class RecordService:
    async def create(self, user_id: str, data: RecordCreate) -> RecordResponse:
        """
        创建新记录
        """
        record_id = str(uuid.uuid4())

        # 插入记录
        async with db.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO records (id, user_id, content, created_at)
                VALUES ($1, $2, $3, $4)
                """,
                record_id,
                user_id,
                data.content,
                datetime.now(),
            )

        return RecordResponse(
            id=record_id,
            content=data.content,
            created_at=datetime.now(),
            analyzed=False,
        )

    async def analyze_record(self, record_id: str, user_id: str) -> StructuredData:
        """
        对单条记录进行结构化分析
        """
        # 获取记录内容
        async with db.pool.acquire() as conn:
            record = await conn.fetchrow(
                "SELECT id, content FROM records WHERE id = $1 AND user_id = $2",
                record_id,
                user_id,
            )

        if not record:
            raise ValueError("记录不存在")

        # 调用 AI 进行结构化分析
        structure = await ai_service.analyze_structure(record["content"])

        # 更新记录
        async with db.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE records
                SET raw_structure = $1, emotion = $2, context = $3, theme = $4, analyzed = true
                WHERE id = $5
                """,
                structure.model_dump(),
                structure.emotion,
                structure.context,
                structure.theme,
                record_id,
            )

        return structure

    async def get_record(self, record_id: str, user_id: str) -> Optional[RecordResponse]:
        """
        获取单条记录
        """
        async with db.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, content, raw_structure, created_at, analyzed
                FROM records
                WHERE id = $1 AND user_id = $2
                """,
                record_id,
                user_id,
            )

        if not row:
            return None

        return RecordResponse(
            id=str(row["id"]),
            content=row["content"],
            created_at=row["created_at"],
            analyzed=row["analyzed"],
            structure=StructuredData(**row["raw_structure"]) if row["raw_structure"] else None,
        )

    async def list_records(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> list[RecordResponse]:
        """
        获取记录列表
        """
        async with db.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, content, raw_structure, created_at, analyzed
                FROM records
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3
                """,
                user_id,
                limit,
                offset,
            )

        records = []
        for row in rows:
            records.append(
                RecordResponse(
                    id=str(row["id"]),
                    content=row["content"],
                    created_at=row["created_at"],
                    analyzed=row["analyzed"],
                    structure=StructuredData(**row["raw_structure"]) if row["raw_structure"] else None,
                )
            )

        return records


record_service = RecordService()

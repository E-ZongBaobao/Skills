"""
数据库连接和基础操作
"""
import asyncpg
from typing import Optional
from src.config import settings


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """建立数据库连接池"""
        self.pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL,
            min_size=2,
            max_size=10,
        )
        print("Database connected")

    async def disconnect(self):
        """关闭数据库连接"""
        if self.pool:
            await self.pool.close()
            print("Database disconnected")

    async def init_db(self):
        """初始化数据库表结构"""
        async with self.pool.acquire() as conn:
            # 创建记录表
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID DEFAULT '00000000-0000-0000-0000-000000000000',
                    content TEXT NOT NULL,
                    raw_structure JSONB,
                    embedding VECTOR(3072),
                    emotion VARCHAR(50),
                    context VARCHAR(50),
                    theme VARCHAR(100),
                    created_at TIMESTAMP DEFAULT NOW(),
                    analyzed BOOLEAN DEFAULT FALSE
                )
            """)

            # 创建模式表
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS patterns (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID DEFAULT '00000000-0000-0000-0000-000000000000',
                    pattern_type VARCHAR(50),
                    pattern_key VARCHAR(100),
                    occurrence_count INT,
                    first_seen TIMESTAMP,
                    last_seen TIMESTAMP,
                    sample_record_ids UUID[],
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)

            # 创建洞察表
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS insights (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID DEFAULT '00000000-0000-0000-0000-000000000000',
                    pattern_ids UUID[],
                    content JSONB,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)

            # 创建索引
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_records_user_created
                ON records(user_id, created_at DESC)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_records_emotion
                ON records(emotion) WHERE analyzed = true
            """)

        print("Database tables initialized")


db = Database()

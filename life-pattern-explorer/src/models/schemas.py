"""
数据模型定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# === 输入请求 ===
class RecordCreate(BaseModel):
    content: str = Field(..., min_length=1, description="记录内容")
    record_type: str = Field(default="text", description="类型：text 或 voice")


# === 结构化输出 ===
class StructuredData(BaseModel):
    emotion: str = Field(..., description="主要情绪")
    emotion_intensity: int = Field(..., ge=1, le=5, description="情绪强度 1-5")
    context: str = Field(..., description="场景")
    theme: str = Field(..., description="核心主题")
    conflict: Optional[str] = Field(None, description="潜在冲突")
    key_phrases: List[str] = Field(default_factory=list, description="关键短语")
    summary: str = Field(..., description="一句话摘要")


# === 记录响应 ===
class RecordResponse(BaseModel):
    id: str
    content: str
    created_at: datetime
    analyzed: bool = False
    structure: Optional[StructuredData] = None


# === 模式定义 ===
class Pattern(BaseModel):
    id: str
    type: str  # emotion | context | conflict
    key: str
    count: int
    description: str
    first_seen: datetime
    last_seen: datetime
    sample_record_ids: List[str]


# === 洞察输出 ===
class Insight(BaseModel):
    id: str
    observation: str = Field(..., description="观察（What）")
    pattern: str = Field(..., description="模式（Pattern）")
    possible_explanation: str = Field(..., description="可能解释（Why）")
    reflection_question: str = Field(..., description="反思问题（Question）")
    confidence: str = Field(..., description="置信度：high|medium|low")
    related_record_ids: List[str] = Field(default_factory=list)
    created_at: datetime


# === 洞察列表响应 ===
class InsightsResponse(BaseModel):
    date: str
    insights: List[Insight]
    record_count: int
    next_insight_eta: Optional[str] = None

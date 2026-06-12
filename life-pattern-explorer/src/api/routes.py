"""
API 路由定义
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.models.schemas import RecordCreate, RecordResponse, InsightsResponse
from src.services import record_service, pattern_service
from src.config import settings

router = APIRouter()

# 默认用户 ID（MVP 单用户模式）
DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000000"


@router.post("/records", response_model=RecordResponse)
async def create_record(
    background_tasks: BackgroundTasks, data: RecordCreate
):
    """
    创建新记录

    提交后立即返回，分析异步进行（延迟反馈原则）
    """
    user_id = DEFAULT_USER_ID

    # 创建记录
    record = await record_service.create(user_id, data)

    # 后台任务：分析记录
    background_tasks.add_task(
        analyze_and_check_pattern, record.id, user_id
    )

    return record


@router.get("/records")
async def list_records(limit: int = 20, offset: int = 0):
    """
    获取记录列表
    """
    user_id = DEFAULT_USER_ID
    records = await record_service.list_records(user_id, limit, offset)
    return {"records": records, "total": len(records)}


@router.get("/records/{record_id}")
async def get_record(record_id: str):
    """
    获取单条记录
    """
    user_id = DEFAULT_USER_ID
    record = await record_service.get_record(record_id, user_id)

    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")

    return {"record": record}


@router.get("/insights")
async def get_insights(limit: int = 10):
    """
    获取洞察列表
    """
    user_id = DEFAULT_USER_ID
    insights = await pattern_service.get_insights(user_id, limit)

    # 获取记录总数
    async with record_service.db.pool.acquire() as conn:
        record_count = await conn.fetchval(
            "SELECT COUNT(*) FROM records WHERE user_id = $1", user_id
        )

    # 计算下次触发
    async with record_service.db.pool.acquire() as conn:
        pending_count = await conn.fetchval(
            "SELECT COUNT(*) FROM records WHERE user_id = $1 AND analyzed = false",
            user_id,
        )

    eta = None
    remaining = pattern_service.min_records_for_insight - pending_count
    if remaining > 0:
        eta = f"约 {remaining} 条记录后触发下一次分析"

    return InsightsResponse(
        date=datetime.now().strftime("%Y-%m-%d"),
        insights=insights,
        record_count=record_count,
        next_insight_eta=eta,
    )


@router.post("/analyze/{record_id}")
async def analyze_record(record_id: str):
    """
    手动触发分析（调试用）
    """
    user_id = DEFAULT_USER_ID

    try:
        structure = await record_service.analyze_record(record_id, user_id)
        return {"status": "success", "structure": structure}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


async def analyze_and_check_pattern(record_id: str, user_id: str):
    """
    后台任务：分析记录并检查是否触发模式分析
    """
    try:
        # 1. 分析单条记录
        await record_service.analyze_record(record_id, user_id)

        # 2. 检查是否触发模式分析
        if await pattern_service.check_trigger(user_id):
            # 3. 检测模式
            patterns = await pattern_service.detect_patterns(user_id)

            # 4. 生成洞察
            if patterns:
                await pattern_service.generate_insight(user_id, patterns)

    except Exception as e:
        print(f"后台任务错误：{e}")


from datetime import datetime

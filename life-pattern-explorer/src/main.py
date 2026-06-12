"""
主应用入口
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import settings
from src.db.database import db
from src.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    await db.connect()
    await db.init_db()
    print(f"{settings.APP_NAME} 启动成功")

    yield

    # 关闭时
    await db.disconnect()


app = FastAPI(
    title=settings.APP_NAME,
    description="AI 人生模式探索器 MVP - 从碎片记录中发现重复模式",
    version="0.1.0",
    lifespan=lifespan,
)

# 注册路由
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """健康检查"""
    return {"status": "ok", "app": settings.APP_NAME}


@app.get("/health")
async def health():
    """健康检查端点"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

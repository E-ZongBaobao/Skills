# AI 人生模式探索器 (Life Pattern Explorer)

MVP 版本 - 从碎片记录中发现重复模式的 AI 系统

## 快速开始

### 1. 环境准备

```bash
# 安装 Python 依赖
pip install -e .

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 OPENROUTER_API_KEY
```

### 2. 数据库设置

```bash
# 安装 PostgreSQL
# macOS: brew install postgresql@15

# 创建数据库
createdb life_patterns

# 启用 pgvector 扩展
psql life_patterns -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 3. 运行服务

```bash
# 开发模式
uvicorn src.main:app --reload --port 8000

# 或直接运行
python -m src.main
```

### 4. API 测试

```bash
# 创建记录
curl -X POST http://localhost:8000/api/v1/records \
  -H "Content-Type: application/json" \
  -d '{"content": "今天和领导沟通很紧张，又开始怀疑自己能力不行"}'

# 获取洞察
curl http://localhost:8000/api/v1/insights
```

## API 文档

启动后访问: http://localhost:8000/docs

## 项目结构

```
src/
├── main.py           # 应用入口
├── config.py         # 配置
├── prompts.py        # Prompt 模板
├── api/
│   └── routes.py     # API 路由
├── db/
│   └── database.py   # 数据库连接
├── models/
│   └── schemas.py    # 数据模型
└── services/
    ├── ai_service.py          # AI 服务
    ├── pattern_service.py     # 模式识别
    └── record_service.py      # 记录管理
```

## MVP 核心流程

```
用户输入 → 创建记录 → 异步分析 → 模式检测 → 洞察生成
```

## 技术栈

- 后端：FastAPI
- 数据库：PostgreSQL + pgvector
- AI: Claude via OpenRouter

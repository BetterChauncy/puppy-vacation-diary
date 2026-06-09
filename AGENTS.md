# AGENTS.md

**小狗的度假日记** — FastAPI + PostgreSQL 项目，使用 `uv` 管理包。

## 关键命令

| 命令 | 说明 |
|---|---|
| `uv run pytest -v` | 运行测试（SQLite 测试数据库，无需 PostgreSQL） |
| `uv run uvicorn puppy_vacation_diary.main:app --reload` | 本地后端开发服务器 |
| `cd frontend && npm run dev` | 前端 Vite 开发服务器（`:5173`，代理 `/api` → `:8000`） |
| `cd frontend && npm run build` | 构建前端到 `frontend/dist/`，后端自动挂载 |
| `uv run alembic revision --autogenerate -m "msg"` | 生成迁移 |
| `uv run alembic upgrade head` | 执行迁移 |
| `docker compose up --build` | 启动 app + PostgreSQL |

## 架构

- `src/puppy_vacation_diary/` — 应用包（`main.py` 为入口）
- `src/puppy_vacation_diary/core/` — 配置、数据库引擎、依赖注入、存储抽象、缩略图
- `src/puppy_vacation_diary/models/` — SQLAlchemy ORM 模型（`base.py` 为 Base）
- `src/puppy_vacation_diary/schemas/` — Pydantic 请求/响应模型
- `src/puppy_vacation_diary/routers/` — API 路由（health, config, pets, media）
- `frontend/` — Vue 3 + Vite SPA（主页 + 管理页）
- `tests/` — pytest + httpx.AsyncClient，使用 SQLite 代替 PostgreSQL
- `alembic/` — async 迁移

## 注意事项

- `uv sync` 需要先执行（已安装 `.venv`）
- 数据库迁移需要 PostgreSQL 运行中；测试用 SQLite 自动处理
- `pyproject.toml` 中 `name = "puppy-vacation-diary"`，对应包路径 `puppy_vacation_diary`
- 主页默认宠物通过 `config.py` 的 `homepage_pet_id` 或 `.env` 环境变量配置
- 开发时同时启动两个终端：`uvicorn`（后端）和 `npm run dev`（前端，自动代理 `/api`）
- 生产构建后，后端自动从 `frontend/dist/` 提供前端 SPA

# 🐶 小狗的度假日记

记录和分享宠物日常的照片与视频。支持批量上传、自动生成缩略图、主页轮播、点赞评论分享。

## 技术栈

| 层级 | 技术 |
|---|---|
| 后端 | Python 3.12, FastAPI, SQLAlchemy (async), Alembic |
| 前端 | Vue 3 (Composition API), TypeScript, Vite |
| 数据库 | PostgreSQL 17 |
| 存储 | 本地文件系统（可扩展 S3） |
| 容器 | Docker Compose (app + PostgreSQL) |
| 包管理 | `uv` (Python), `npm` (前端) |

## 功能

- **宠物管理** — 添加/编辑/删除宠物资料（名称、品种、性别、年龄、生日、简介、头像）
- **媒体管理** — 批量上传照片和视频，自动生成 400×400 WEBP 缩略图（Pillow + ffmpeg）
- **主页轮播** — 选择多只宠物设为首页展示，支持每日/每小时间隔轮换
- **媒体预览** — 点击缩略图全屏预览照片/视频，支持下载
- **互动** — 点赞（❤️）、评论（增删）、分享（复制链接）
- **响应式** — 适配移动端和桌面端

## 快速开始

### 前置要求

- Python 3.12+
- Node.js 18+
- Docker Desktop（用于 PostgreSQL）
- ffmpeg（视频缩略图）
- `uv` 包管理器

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 启动

```bash
# 1. 安装后端依赖
uv sync

# 2. 启动 PostgreSQL
docker compose up -d db

# 3. 执行数据库迁移
uv run alembic upgrade head

# 4. 启动后端（终端 1）
uv run uvicorn puppy_vacation_diary.main:app --reload --port 8000

# 5. 启动前端（终端 2）
cd frontend && npm install && npm run dev
```

打开浏览器访问 http://localhost:5173

### 运行测试

```bash
uv run pytest -v
```

测试使用 SQLite，无需 PostgreSQL。

## 项目结构

```
src/puppy_vacation_diary/
├── main.py              # FastAPI 入口（CORS、静态文件）
├── core/
│   ├── config.py        # pydantic-settings 配置
│   ├── database.py      # 异步数据库引擎
│   ├── dependencies.py  # 依赖注入（DB session）
│   ├── storage.py       # 存储抽象（Local / S3）
│   └── thumbnails.py    # 缩略图生成
├── models/              # SQLAlchemy ORM 模型
├── schemas/             # Pydantic 请求/响应
└── routers/             # API 路由
frontend/
├── src/
│   ├── api/index.ts     # Axios API 封装
│   ├── components/      # 可复用组件
│   └── views/           # 页面（Home / Admin）
└── vite.config.ts       # Vite 配置（代理 /api → :8000）
```

## 命令参考

| 命令 | 说明 |
|---|---|
| `uv run pytest -v` | 运行测试 |
| `uv run uvicorn puppy_vacation_diary.main:app --reload` | 启动后端开发服务器 |
| `cd frontend && npm run dev` | 启动前端 Vite 开发服务器 |
| `cd frontend && npm run build` | 构建前端到 `frontend/dist/` |
| `uv run alembic upgrade head` | 执行数据库迁移 |
| `uv run alembic revision --autogenerate -m "msg"` | 生成迁移文件 |
| `docker compose up --build` | 启动完整项目（app + PostgreSQL） |

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/demo1` | 数据库连接 |
| `CORS_ORIGINS` | `http://localhost:5173` | 允许的跨域来源（逗号分隔） |
| `UPLOAD_DIR` | `uploads` | 文件上传目录 |
| `MAX_UPLOAD_SIZE` | `52428800` (50MB) | 单次上传最大字节数 |
| `THUMBNAIL_SIZE` | `400` | 缩略图尺寸（正方形） |

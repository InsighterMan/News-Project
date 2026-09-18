# LIVE NEWS · 本地 AI 新闻资讯平台

> 一个面向求职展示的全栈新闻资讯项目：提供实时资讯流、新闻检索、收藏/点赞/历史记录、个人中心、多主题与中英文切换，并接入本地运行的 DeepSeek-R1 7B 实现登录后 AI 问答。

![Vue 3](https://img.shields.io/badge/Vue-3-42b883?logo=vuedotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111111)

## 项目简介

LIVE NEWS 是一个以“阅读、沉淀、问答”为核心流程的新闻应用。项目不只实现资讯展示，还围绕真实使用场景补全了用户状态、内容交互、个性化外观与本地 AI 能力：

- 读者可以按频道浏览实时资讯并进入详情页；
- 可通过关键词检索当前资讯流；
- 登录后可收藏、点赞、查看历史记录和维护个人资料；
- 可以在四种玻璃拟态主题与中英文界面之间切换；
- AI 问答通过后端连接本机 Ollama 的 DeepSeek-R1 7B，不向第三方云模型发送对话内容。

该项目作为前端、全栈或 AI 应用开发方向的作品集项目，重点体现了 UI 一致性、前后端接口设计、认证保护以及本地大模型接入能力。

## 项目展示
- **首页模块**

<img width="1897" height="979" alt="image" src="https://github.com/user-attachments/assets/7b1b6728-8351-4e9f-be5f-db7f2d37b408" />

- **新闻详情**

<img width="1898" height="974" alt="image" src="https://github.com/user-attachments/assets/62bf72a9-baa4-42c2-9d85-c7132b32d623" />

- **搜索功能**

<img width="1900" height="974" alt="image" src="https://github.com/user-attachments/assets/35627db7-4c3c-4804-b376-1974337120ff" />

- **AI对话模块**

<img width="1899" height="975" alt="image" src="https://github.com/user-attachments/assets/616b934f-3113-47c5-9711-ae6d80ea0ee9" />

- **"我的"模块**

<img width="1911" height="978" alt="image" src="https://github.com/user-attachments/assets/a5109205-7c31-49e2-9303-725ebb631312" />


## 核心功能

| 模块 | 已实现能力 |
| --- | --- |
| 实时资讯 | 分类资讯流、资讯详情、来源跳转、去重、数据源异常兜底、SSE 实时流接口 |
| 搜索 | 首页搜索栏按关键词筛选当前资讯流；收起搜索栏后自动清除关键词 |
| 内容交互 | 登录后收藏、点赞、浏览历史；未登录操作会引导至登录/注册 |
| 用户系统 | 注册、登录、Token 鉴权、个人资料、头像、简介、密码修改 |
| 个人中心 | 收藏、点赞与历史记录的统计、空状态和快捷跳转 |
| 主题与语言 | 四套可切换主题变量、全局玻璃拟态视觉、中英文页面文案 |
| 本地 AI | 受登录保护的 AI 对话接口，后端调用 Ollama `deepseek-r1:7b`，支持上下文与中英文系统提示词 |

## 技术架构

```text
┌─────────────────────────────────────────────────────────────┐
│ Vue 3 + Vite + Pinia + Vue Router + Vant                    │
│ 资讯流 / 搜索 / 收藏点赞 / 主题语言 / AI Chat               │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP + Authorization Token
┌────────────────────────▼────────────────────────────────────┐
│ FastAPI                                                       │
│ 用户、新闻、收藏、历史、实时资讯、AI 路由                    │
└───────────────┬──────────────────────────┬──────────────────┘
                │                          │
        ┌───────▼────────┐        ┌────────▼──────────────┐
        │ MySQL 8        │        │ Ollama (local)         │
        │ 用户与业务数据 │        │ deepseek-r1:7b         │
        └────────────────┘        └───────────────────────┘
```

### 技术选型

- 前端：Vue 3、Vite、Pinia、Vue Router、Axios、Vant、vue-i18n
- 后端：FastAPI、SQLAlchemy Async、Pydantic、Uvicorn
- 数据库：MySQL 8（通过 `aiomysql` 异步访问）
- 本地模型：Ollama + DeepSeek-R1 7B
- 资讯服务：实时资讯路由会优先请求聚合源，异常或空结果时使用中国新闻网公开资讯作为回退来源

## 本地 AI 设计

AI 功能采用“浏览器 → 项目后端 → 本地 Ollama”的调用链：

1. 前端不会直接访问 Ollama，避免将本地模型服务暴露给浏览器；
2. `POST /api/ai/chat` 使用登录 Token 鉴权，未登录用户不能调用模型；
3. 后端通过 `http://127.0.0.1:11434/api/chat` 请求 `deepseek-r1:7b`；
4. 根据当前界面语言注入中文或英文系统提示词；
5. 前端仅展示最终回答，不展示模型内部推理内容。


## 目录结构

```text
News Project/
├── toutiao_frontend/
│   └── frontend_code/
│       ├── src/
│       │   ├── components/      # 底部导航、资讯列表等复用组件
│       │   ├── config/          # 后端与 AI 接口地址
│       │   ├── router/          # 前端路由
│       │   ├── store/           # 用户、主题、资讯等状态
│       │   ├── utils/           # 文案与资讯翻译工具
│       │   └── views/           # 页面级组件
│       └── package.json
├── toutiao_backend/
│   ├── routers/                 # 用户、新闻、收藏、历史、实时资讯、AI 路由
│   ├── crud/                    # 数据访问层
│   ├── models/                  # SQLAlchemy 数据模型
│   ├── schemas/                 # Pydantic 请求/响应模型
│   ├── services/                # 资讯抓取服务
│   ├── utils/                   # 鉴权、响应与异常处理
│   └── main.py
└── README.md
```

## 快速开始

### 1. 环境要求

- Node.js 18+
- Python 3.11+
- MySQL 8+
- [Ollama](https://ollama.com/)（若需使用 AI 问答）

### 2. 准备数据库

创建 MySQL 数据库并导入本项目对应的数据表结构与初始数据。随后按本地环境修改：

```python
# toutiao_backend/config/db_conf.py
ASYNC_DATABASE_URI = "mysql+aiomysql://<user>:<password>@127.0.0.1:3306/<database>?charset=utf8mb4"
```

> 建议在实际部署中使用环境变量管理数据库连接，而不要把密码提交至仓库。

### 3. 启动后端

```bash
cd toutiao_backend

# 建议使用虚拟环境
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell
# source .venv/bin/activate       # macOS / Linux

pip install fastapi "uvicorn[standard]" sqlalchemy aiomysql passlib[bcrypt]
python main.py
```

后端默认地址：`http://127.0.0.1:8000`  
接口文档：`http://127.0.0.1:8000/docs`

### 4. 启动本地模型（可选）

```bash
ollama pull deepseek-r1:7b
ollama serve
```

默认模型服务地址为 `http://127.0.0.1:11434`。可以通过环境变量覆盖模型配置：

```bash
# Windows PowerShell 示例
$env:OLLAMA_MODEL = "deepseek-r1:7b"
$env:OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
```

### 5. 启动前端

```bash
cd toutiao_frontend/frontend_code
npm install
npm run dev
```

浏览器访问 Vite 控制台输出的地址（通常为 `http://127.0.0.1:5173`）。

### 6. 生产构建

```bash
cd toutiao_frontend/frontend_code
npm run build
```

## 关键接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/api/user/register` | 用户注册 |
| `POST` | `/api/user/login` | 用户登录并获取 Token |
| `GET` | `/api/live/news` | 获取实时资讯流，支持分类和关键词 |
| `GET` | `/api/live/stream` | 实时资讯 SSE 流 |
| `POST` | `/api/favorite/add` | 收藏资讯（需登录） |
| `GET` | `/api/history/list` | 获取浏览历史（需登录） |
| `POST` | `/api/ai/chat` | 调用本地 DeepSeek AI（需登录） |


## 后续可扩展方向

- 使用 Redis 缓存热点资讯和模型回答，降低重复请求；
- 为 AI 对话增加流式输出、会话持久化与引用新闻上下文；
- 引入数据库迁移工具（如 Alembic）和依赖清单（`requirements.txt`）；
- 为前后端增加单元测试、接口测试和端到端测试；
- 使用环境变量、反向代理和 HTTPS 完善部署安全性。

## 说明

本demo仅用于学习、作品集展示与本地开发。资讯内容以原始新闻来源为准；AI 回答仅作辅助参考，不应替代对新闻原始报道的核验。

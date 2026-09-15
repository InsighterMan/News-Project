# 🚀 FastAPI News Backend Project

基于 FastAPI + SQLAlchemy + Pydantic + MySQL 开发的高性能新闻资讯系统后端。项目实现了用户认证、JWT 令牌管理、新闻分类检索、文章收藏、浏览历史记录等核心功能，适合作为个人作品集或后端开发练手项目。

---

## 🛠️ 技术栈

* 核心框架: FastAPI (Python 3.11+)
* 异步/服务器: Uvicorn
* 数据库/ORM: MySQL, SQLAlchemy
* 数据校验: Pydantic
* 权限管理: JWT (JSON Web Token)

---

## ✨ 核心功能模块

* 用户系统: 支持用户注册、登录、JWT 身份认证及个人信息管理。
* 新闻资讯: 支持多分类新闻浏览、查看量统计、详情页及关键词搜索。
* 个性化互动:
  * 文章收藏: 用户可对感兴趣的新闻进行收藏与取消收藏管理。
  * 浏览历史: 自动记录用户的文章浏览轨迹，支持历史足迹查询。
* 静态与动态资源: 集成静态文件托管与动态图床适配，确保前端页面资源平稳加载。

---

## 📂 项目结构概览

toutiao_backend/
│
├── main.py              # 程序主入口（挂载路由、CORS、异常处理与启动配置）
├── config/              # 配置文件与数据库连接池
├── models/              # SQLAlchemy 数据库模型定义
├── schemas/             # Pydantic 数据校验与传输模型
├── routers/             # 路由控制层
│   ├── news_rou.py      # 新闻资讯相关路由
│   ├── users_rou.py     # 用户认证与信息路由
│   ├── favorite_rou.py  # 收藏功能路由
│   └── history_rou.py   # 浏览历史路由
├── utils/               # 工具类（异常处理、JWT工具、密码加密等）
└── requirements.txt     # 项目依赖包列表

---

## 📖 API 接口文档

项目启动后，你可以直接访问以下内置的交互式接口文档进行测试：
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

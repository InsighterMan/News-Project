# 🚀 FastAPI News Backend Project

基于 FastAPI + SQLAlchemy + Pydantic + MySQL + Agent 开发的高性能新闻资讯系统后端。项目实现了用户认证、JWT 令牌管理、新闻分类检索、文章收藏、浏览历史记录等核心功能，为个人后端开发项目，实现代码仅展示后端而非全栈。

---

## 🛠️ 技术栈

* 核心框架: FastAPI (Python 3.11+)
* 异步/服务器: Uvicorn
* 数据库/ORM: MySQL, SQLAlchemy
* 数据校验: Pydantic
* 权限管理: JWT (JSON Web Token)
* AI对话：千问大模型, 百炼Agent

---

## ✨ 核心功能模块

* 用户系统: 支持用户注册、登录、JWT 身份认证及个人信息管理。
* 新闻资讯: 支持多分类新闻浏览、查看量统计、详情页及关键词搜索。
* 个性化互动:
  * 文章收藏: 用户可对感兴趣的新闻进行收藏与取消收藏管理。
  * 浏览历史: 自动记录用户的文章浏览轨迹，支持历史足迹查询。
* 静态与动态资源: 集成静态文件托管与动态图床适配，确保前端页面资源平稳加载。
* AI对话：借助千问大模型的agent百炼实现AI chat功能。（该功能仅做展示，具体实现代码封装在前端）

---

## 📂 项目结构概览

```
toutiao_backend/
│
├── main.py              # 程序主入口（挂载路由、CORS、异常处理与启动配置）
├── config/              # 配置文件与数据库连接池
├── models/              # SQLAlchemy 数据库模型定义
├── schemas/             # Pydantic 数据校验与传输模型
├── routers/             # 路由层
│   ├── news_rou.py      # 新闻资讯相关路由
│   ├── users_rou.py     # 用户认证与信息路由
│   ├── favorite_rou.py  # 收藏功能路由
│   └── history_rou.py   # 浏览历史路由
├── utils/               # 工具类（异常处理、JWT工具、密码加密等）
└── requirements.txt     # 项目依赖包列表
```

---

## 📖 API 接口文档

项目启动后，你可以直接访问以下内置的交互式接口文档进行测试：
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc
* Agent：填写对应的api key实现AI对话功能

---

## 🖼️ 项目预览

* 首页新闻实现板块

<img width="1910" height="980" alt="image" src="https://github.com/user-attachments/assets/5bac18b1-66b4-43fb-8630-7e147ef68add" />
<img width="1909" height="980" alt="image" src="https://github.com/user-attachments/assets/e3c2ab32-cdf0-4edd-80f0-0518794a7371" />
<img width="1919" height="979" alt="image" src="https://github.com/user-attachments/assets/a4e48814-b1ae-49d9-a0d9-f00e2b8bcab1" />


* AI对话功能实现板块

<img width="389" height="840" alt="99273b23cce2e91cab3dcef7f21f5afb" src="https://github.com/user-attachments/assets/87b4a53a-5033-492b-b978-8556b7a37efa" />

* 个人主页实现板块
<img width="1913" height="979" alt="image" src="https://github.com/user-attachments/assets/ba803457-cb98-4d80-ab45-8dda71f83d0d" />

---


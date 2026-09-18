import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import ai_rou, news_rou, users_rou, favorite_rou, history_rou, live_news_rou
from utils.exc_handler import register_exception_handlers

app = FastAPI()

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,   # 允许携带cookie
    allow_methods=["*"],    # 允许的请求方法
    allow_headers=["*"],    # 允许的请求头
)

# 注册异常处理器
register_exception_handlers(app)

# 挂载路由
app.include_router(news_rou.router)
app.include_router(users_rou.router)
app.include_router(favorite_rou.router)
app.include_router(history_rou.router)
app.include_router(live_news_rou.router)
app.include_router(ai_rou.router)

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

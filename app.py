from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controller.basic_controller import router as basic_router

# 创建 FastAPI 实例
app = FastAPI()

# 添加 CORS 中间件，允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # 允许跨域的源
    allow_credentials=True,  # 允许发送 cookies 等凭证
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET, POST, PUT 等）
    allow_headers=["*"],  # 允许所有请求头
)

# 引入控制器中的路由
app.include_router(basic_router)

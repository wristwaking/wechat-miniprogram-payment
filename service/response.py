from typing import Any
from pydantic import BaseModel


# 定义统一的响应格式
class ResponseModel(BaseModel):
    code: int
    message: str
    data: Any


# 创建一个统一的成功响应函数
def success(code: int = 200, data: Any = None, message: str = "请求成功") -> ResponseModel:
    return ResponseModel(code=code, message=message, data=data)


# 创建一个统一的失败响应函数
def error(code: int = 400, message: str = "请求失败", data: Any = None) -> ResponseModel:
    return ResponseModel(code=code, message=message, data=data)

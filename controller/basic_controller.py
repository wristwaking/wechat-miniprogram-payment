import aiohttp
from fastapi import APIRouter, Request
from fastapi.params import Body

from open import wechat_pay
from service.response import success, error

# 创建路由器实例
router = APIRouter()


@router.post("/login")
async def login(request: Request, params: dict = Body(...)):
    code = params.get("code")
    params = {
        "appid": "【微信小程序 APPID】",
        "certificates": "【微信小程序 APP SECRET】",
        "js_code": code,
        "grant_type": "authorization_code"
    }
    async with aiohttp.ClientSession() as session:
        # 使用 GET 方法获取响应
        async with session.get("https://api.weixin.qq.com/sns/jscode2session", params=params) as response:
            # 返回响应的文本内容
            data = await response.json()
    return success(code=200, message="登录成功", data=data)


@router.post("/wechat/pay")
async def login(request: Request, params: dict = Body(...)):
    openid = params.get("openid")
    amount_total = params.get("amount_total")
    description = params.get("description")
    data = await wechat_pay.create_wechat_pay(openid=openid, description=description, amount_total=amount_total)
    return success(code=200, message="请求成功", data=data)

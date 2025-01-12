import time
import aiohttp
import asyncio
import json
from open import authorization, paysign
import os
import struct


def hexdump_random_bytes(num_bytes=16, chunk_size=4):
    random_bytes = os.urandom(num_bytes)
    result = []
    for i in range(0, len(random_bytes), chunk_size):
        value = struct.unpack('>I', random_bytes[i:i + chunk_size])[0]
        result.append(f'{value:08X}')
    return ''.join(result)


async def post_payment(params):
    url = "https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi"

    body = {
        "appid": params['appid'],
        "mchid": params['mchid'],
        "description": params['description'],
        "out_trade_no": params['out_trade_no'],
        "notify_url": params['notify_url'],
        "support_fapiao": True,
        "amount": {
            "total": params['amount_total'],
            "currency": "CNY"
        },
        "payer": {
            "openid": params['openid']
        },
        "settle_info": {
            "profit_sharing": False
        }
    }

    signature = authorization.signature_base64(
        nonce_str=params['nonce_str'],
        timestamp=params['timestamp'],
        body=body
    )

    Authorization = f"WECHATPAY2-SHA256-RSA2048 mchid=\"{params['mchid']}\",nonce_str=\"{params['nonce_str']}\",signature=\"{signature}\",timestamp=\"{params['timestamp']}\",serial_no=\"{params['serial_no']}\""
    headers = {
        "Authorization": Authorization,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    json_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=json_str) as response:
                if response.status == 200:
                    result = await response.json()
                    print("支付请求成功:", result)
                    return result.get("prepay_id")
                else:
                    result = await response.text()
                    print(f"支付请求失败，状态码: {response.status}, 错误信息: {result}")
                    return None
        except Exception as e:
            print(f"请求发生异常: {str(e)}")
            return None


def get_payment_params(params):
    return {
        "timeStamp": params['timestamp'],
        "nonceStr": params['nonce_str'],
        "package": f"prepay_id={params['prepay_id']}",
        "signType": "RSA",
        "paySign": params['pay_sign']
    }


async def create_wechat_pay(openid: str, description: str, amount_total: int):
    out_trade_no = hexdump_random_bytes()
    nonce_str = hexdump_random_bytes()
    params = {
        'appid': "【微信小程序 APPID】",
        'mchid': "【微信商户 ID】",
        'description': description,
        'out_trade_no': out_trade_no,
        'notify_url': "https://www.weixin.qq.com/wxpay/pay.php",
        'openid': openid,
        'serial_no': "【微信支付证书序列号】",
        'amount_total': amount_total,
        'nonce_str': nonce_str,
        'timestamp': str(int(time.time()))
    }
    prepay_id = await post_payment(params)
    if prepay_id:
        pay_sign = paysign.signature_base64(timestamp=params['timestamp'], nonce_str=params['nonce_str'],
                                            prepay_id=prepay_id)
        params['prepay_id'] = prepay_id
        params['pay_sign'] = pay_sign
        return get_payment_params(params)
    return None


# 在 __main__ 块中
if __name__ == "__main__":
    description = "测试标题"
    amount_total = 1000  # 示例金额（单位：分）
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_wechat_pay(description=description, amount_total=amount_total))

import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


def generate_sign_string():
    # 构建签名字符串
    sign_string = (
        "wx2421b1c4370ec43b\n"
        "1554208460\n"
        "593BEC0C930BF1AFEB40B4A08C8FB242\n"
        "prepay_id=wx201410272009395522657a690389285100\n"
    )
    return sign_string



def sign_with_private_key(sign_string, private_key_path):
    # 载入私钥
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    # 对待签名字符串进行 SHA256 签名
    signature = private_key.sign(
        sign_string.encode("utf-8"),
        padding.PKCS1v15(),  # 修改为从 padding 模块中导入
        algorithm=hashes.SHA256()
    )

    # 对签名结果进行 Base64 编码
    base64_signature = base64.b64encode(signature).decode('utf-8')

    return base64_signature


def signature_base64():
    # 获取待签名字符串
    sign_string = generate_sign_string()

    # 私钥路径（替换为你本地的私钥路径）
    private_key_path = "../certificates/wechat_private_key_template.pem"

    # 获取签名并进行 Base64 编码
    signature_base64 = sign_with_private_key(sign_string, private_key_path)

    print("Base64编码后的签名:", signature_base64)
    return signature_base64


print(signature_base64())

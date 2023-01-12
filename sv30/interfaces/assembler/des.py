import pyDes
import base64
from infrastructure.config.config import Config

config = Config()
des_key = config.get_des_key().get("des_key")


def des_en(text):
    iv = secret_key = des_key
    k = pyDes.des(secret_key, pyDes.CBC, IV=iv, pad=None, padmode=pyDes.PAD_PKCS5)
    text = str(text).encode()
    data = k.encrypt(text)
    # data.进制返回文本字符串.解码字符串
    base = base64.b64encode(data)
    base = str(base64.b64encode(base), encoding="utf-8")
    return base


# 解密
def des_de(text):
    iv = secret_key = des_key
    k = pyDes.des(secret_key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    base = base64.b64decode(text)
    base = base64.b64decode(base)
    data = (k.decrypt(base)).decode()
    return data

"""
网络请求模块
负责与校园网登录接口通信
"""

import json
import re

import requests
import urllib3
from fake_useragent import UserAgent

# 禁用 SSL 警告（校园网使用自签名证书）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 校园网登录接口地址（固定不变）
LOGIN_URL = "http://172.18.2.6/drcom/login"

_ua = UserAgent()


def _build_headers() -> dict:
    """构建请求头，每次随机 UA"""
    return {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Referer": "http://172.18.2.6/a79.htm",
        "User-Agent": _ua.random,
    }

# 请求超时（秒）
TIMEOUT = 10


def login(username: str, password: str) -> dict:
    """
    发送校园网登录请求
    参数:
        username: 账号
        password: 密码
    返回:
        {"ok": True, "message": "连接成功"}
        {"ok": False, "message": "错误信息"}
    """
    params = {
        "callback": "dr1003",
        "DDDDD": username,
        "upass": password,
        "0MKKey": "123456",
        "R1": "0",
        "R2": "",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "v6ip": "",
        "terminal_type": "1",
        "lang": "zh-cn",
        "jsVersion": "4.2",
        "v": "4841",
    }

    try:
        resp = requests.get(
            LOGIN_URL,
            params=params,
            headers=_build_headers(),
            verify=False,
            timeout=TIMEOUT,
            proxies={"http": None, "https": None},
        )
        resp.raise_for_status()
        raw = resp.text

    except requests.exceptions.Timeout:
        return {"ok": False, "message": "网络超时，请检查网络连接"}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "message": "无法连接校园网，请检查是否已接入校园网络"}
    except Exception as e:
        return {"ok": False, "message": str(e)}

    # 解析 JSONP 响应: dr1003({...})
    match = re.search(r"\{.*\}", raw)
    if not match:
        return {"ok": False, "message": "响应解析失败"}

    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return {"ok": False, "message": "响应解析失败"}

    result = data.get("result", 0)

    if result == 1:
        return {"ok": True, "message": "连接成功"}
    else:
        msg = data.get("msga", "未知错误")
        return {"ok": False, "message": msg}

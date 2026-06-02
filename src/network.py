"""
网络请求模块
负责与校园网登录接口通信
登录地址写死在这里，不存配置文件
"""

import requests

# 校园网登录接口地址（写死，不变）
LOGIN_URL = ""


def login(username: str, password: str) -> bool:
    """
    发送校园网登录请求
    参数:
        username: 账号（学号）
        password: 密码
    返回:
        True 表示登录成功，False 表示登录失败
    """
    # TODO: 具体请求逻辑后面再写
    pass

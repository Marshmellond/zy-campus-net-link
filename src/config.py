"""
配置管理模块
只负责 config.ini 的读取、写入、自动创建
只存储账号和密码两个字段
"""

import configparser
import os
import sys


def _get_config_dir() -> str:
    """获取配置文件目录，自动适配 Windows / macOS / Linux"""
    system = sys.platform

    if system == "win32":
        # Windows: %APPDATA%\zy-campus-net-link
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        return os.path.join(base, "zy-campus-net-link")

    elif system == "darwin":
        # macOS: ~/Library/Application Support/zy-campus-net-link
        return os.path.expanduser(
            "~/Library/Application Support/zy-campus-net-link"
        )

    else:
        # Linux: ~/.config/zy-campus-net-link (遵循 XDG 规范)
        xdg = os.environ.get(
            "XDG_CONFIG_HOME",
            os.path.expanduser("~/.config")
        )
        return os.path.join(xdg, "zy-campus-net-link")


def _get_config_path() -> str:
    """获取 config.ini 完整路径"""
    return os.path.join(_get_config_dir(), "config.ini")


def _ensure_config_exists() -> None:
    """首次运行时自动创建默认配置文件，用户无需手动创建"""
    config_dir = _get_config_dir()
    config_path = _get_config_path()

    if not os.path.exists(config_path):
        os.makedirs(config_dir, exist_ok=True)

        parser = configparser.ConfigParser()
        parser["account"] = {
            "username": "",
            "password": "",
        }

        with open(config_path, "w", encoding="utf-8") as f:
            parser.write(f)


def load_config() -> configparser.ConfigParser:
    """加载配置文件，返回 ConfigParser 对象"""
    _ensure_config_exists()

    parser = configparser.ConfigParser()
    parser.read(_get_config_path(), encoding="utf-8")
    return parser


def save_config(parser: configparser.ConfigParser) -> None:
    """保存配置到文件"""
    config_path = _get_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        parser.write(f)


def get_account() -> dict:
    """读取账号信息，返回 {'username': str, 'password': str}"""
    cfg = load_config()
    return {
        "username": cfg.get("account", "username", fallback=""),
        "password": cfg.get("account", "password", fallback=""),
    }


def set_account(username: str, password: str) -> None:
    """写入账号信息到配置文件"""
    cfg = load_config()
    cfg["account"]["username"] = username
    cfg["account"]["password"] = password
    save_config(cfg)


def get_config_path() -> str:
    """返回配置文件所在路径，供 main 里显示用"""
    return _get_config_path()

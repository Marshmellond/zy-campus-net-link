<p align="center">
  <img src="resources/zy.webp" alt="logo" width="180">
</p>

<h1 align="center">张家界学院校园网自动登录工具</h1>

<p align="center">
  双击运行 · 自动连接 · 省去每次手动登录的麻烦
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue" alt="platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
</p>

---

## ✨ 功能

- 🚀 **自动连接** — 双击启动后自动尝试登录，成功自动退出
- 🔄 **断线重试** — 每 10 秒重试一次，最多 6 次（1 分钟），连上即停
- 🖐️ **手动模式** — 自动模式中途按回车即可切换到手动菜单
- ⚙️ **账号管理** — 交互式查看和修改账号密码，保存即用

## 📥 下载

前往 [Releases](https://github.com/Marshmellond/zy-campus-net-link/releases) 页面下载最新版本 `zy-campus-net-link.exe`。

> 仅提供 Windows 版本，Linux / macOS 用户请参考下方 [开发](#-开发) 自行编译。

## 🚀 使用

1. 从 [Releases](https://github.com/Marshmellond/zy-campus-net-link/releases) 下载 `zy-campus-net-link.exe`
2. 双击运行
3. 首次使用会进入手动菜单，选择 `[2]` 设置学号和密码
4. 之后每次双击即可自动连接

## 📋 手动菜单

```
╭──────────────────────────────────────╮
│  张家界学院校园网自动登录工具        │
│                                      │
│  [1] 连接校园网                      │
│  [2] 查看/修改账号信息               │
│  [3] 退出                            │
│                                      │
╰──────────────────────────────────────╯
```

| 选项 | 说明 |
|------|------|
| `[1]` 连接校园网 | 用已保存的账号密码手动登录 |
| `[2]` 查看/修改账号信息 | 显示当前账号，可修改保存 |
| `[3]` 退出 | 退出程序 |

## 📁 配置文件

配置文件自动创建，无需手动操作：

| 系统 | 路径 |
|------|------|
| Windows | `%APPDATA%\zy-campus-net-link\config.ini` |
| Linux | `~/.config/zy-campus-net-link/config.ini` |
| macOS | `~/Library/Application Support/zy-campus-net-link/config.ini` |

## 🔧 开发

```bash
# 安装依赖
uv sync

# 运行
python src/main.py

# 打包
pyinstaller --onefile --console --name zy-campus-net-link --icon resources/zy.ico --paths src src/main.py
```

## ⚠️ 免责声明

本工具仅供**张家界学院在校学生**用于便捷登录校园网络。请勿将本工具用于任何非法用途。

- 账号密码仅存储在本地配置文件中，不会上传至任何服务器
- 登录请求直接发送至校园网认证服务器（`172.18.2.6`），不经过第三方
- 使用本工具产生的任何网络行为由用户自行承担责任

## 📄 许可

MIT License

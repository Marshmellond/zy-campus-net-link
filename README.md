<p align="center">
  <img src="resources/zy.webp" alt="logo" width="180">
</p>

<h1 align="center">张家界学院校园网自动登录工具</h1>

<p align="center">
  双击运行 · 自动连接 · 省去每次手动登录的麻烦
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Windows-blue" alt="platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/github/v/release/Marshmellond/zy-campus-net-link" alt="release">
</p>

---

## ✨ 功能

- 🚀 **自动连接** — 双击启动自动登录，成功即退出
- 🔄 **断线重试** — 每 10 秒重试，最多 6 次，连上即停
- 🖐️ **中途切换** — 自动模式中按回车随时切到手动操作
- ⚙️ **账号管理** — 交互式查看修改学号和密码

<p align="center">
  <img src="resources/auto-connect.png" alt="自动连接" width="600">
</p>

## 📥 下载

前往 [Releases](https://github.com/Marshmellond/zy-campus-net-link/releases) 下载最新 `zy-campus-net-link.exe`，双击即可使用。

> 仅提供 Windows 版，Linux / macOS 请参考 [开发](#-开发) 自行编译。

首次使用会进入手动菜单，设置学号和密码后再次双击即可自动连接。

<p align="center">
  <img src="resources/home.png" alt="主菜单" width="600">
</p>

| 选项 | 说明 |
|------|------|
| `[1]` 连接校园网 | 手动登录 |
| `[2]` 查看/修改账号信息 | 查看或修改学号和密码 |
| `[3]` 退出 | 退出程序 |

## 📁 配置文件

配置自动创建，无需手动操作：

| 系统 | 路径 |
|------|------|
| Windows | `%APPDATA%\zy-campus-net-link\config.ini` |
| Linux | `~/.config/zy-campus-net-link/config.ini` |
| macOS | `~/Library/Application Support/zy-campus-net-link/config.ini` |

## 🔧 开发

```bash
uv sync                         # 安装依赖
python src/main.py              # 运行
pyinstaller --onefile --console --name zy-campus-net-link --icon resources/zy.ico --paths src src/main.py  # 打包
```

## ⚠️ 免责声明

本工具仅供**张家界学院在校学生**便捷登录校园网络。

- 账号密码仅存储在本地，不上传至任何服务器
- 登录请求直达校园网认证服务器，不经过第三方
- 使用本工具产生的网络行为由用户自行承担

## 📄 许可

MIT License

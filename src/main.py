"""
程序入口模块
交互式菜单，双击 exe 即可使用
"""

import os
import sys

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import config
import network

console = Console()
PANEL_WIDTH = 56


def _clear_screen() -> None:
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


def _build_menu_panel() -> Panel:
    text = Text()
    text.append("[1] 连接校园网\n", style="bold cyan")
    text.append("[2] 查看/修改账号信息\n", style="bold cyan")
    text.append("[3] 退出", style="bold cyan")
    return Panel(
        text,
        title="张家界学院校园网自动登录工具",
        border_style="cyan",
        width=PANEL_WIDTH,
        padding=(1, 3),
    )


def _handle_login() -> None:
    account = config.get_account()

    if not account["username"] or not account["password"]:
        console.print(
            Panel(
                "[bold red]请先设置账号和密码（选项 [2]）[/bold red]",
                title="错误",
                border_style="red",
                width=PANEL_WIDTH,
                padding=(1, 3),
            )
        )
        console.print()
        console.input("[dim]按回车键返回菜单...[/dim]")
        return

    _clear_screen()
    console.print(
        Panel(
            f"正在使用账号 [{account['username']}] 连接校园网...",
            title="连接中",
            border_style="yellow",
            width=PANEL_WIDTH,
            padding=(1, 3),
        )
    )

    result = network.login(account["username"], account["password"])

    if result["ok"]:
        console.print(
            Panel(
                f"[bold green]✓ {result['message']}[/bold green]",
                title="连接结果",
                border_style="green",
                width=PANEL_WIDTH,
                padding=(1, 3),
            )
        )
    else:
        console.print(
            Panel(
                f"[bold red]✗ 连接失败: {result['message']}[/bold red]",
                title="连接结果",
                border_style="red",
                width=PANEL_WIDTH,
                padding=(1, 3),
            )
        )

    console.print()
    console.input("[dim]按回车键返回菜单...[/dim]")


def _handle_config() -> None:
    while True:
        _clear_screen()

        account = config.get_account()

        text = Text()
        text.append("当前账号: ", style="bold")
        text.append(f"{account['username']}\n", style="bold white")
        text.append("当前密码: ", style="bold")
        text.append(f"{account['password']}\n", style="bold white")
        text.append("配置文件:\n", style="bold dim")
        text.append(config.get_config_path(), style="dim")

        console.print(
            Panel(text, title="账号信息", border_style="cyan", width=PANEL_WIDTH, padding=(1, 3))
        )

        console.print()
        console.print("[bold cyan][1][/bold cyan] 修改")
        console.print("[bold cyan][2][/bold cyan] 返回")
        console.print()

        choice = console.input("[bold]> [/bold]").strip()

        if choice == "1":
            console.print()
            username = console.input("[bold]请输入账号: [/bold]").strip()
            password = console.input("[bold]请输入密码: [/bold]").strip()

            if not username or not password:
                console.print()
                console.print(
                    Panel(
                        "[bold red]用户名或密码不能为空，未保存。[/bold red]",
                        border_style="red",
                        width=PANEL_WIDTH,
                    )
                )
                console.print()
                console.input("[dim]按回车键继续...[/dim]")
            else:
                config.set_account(username, password)
                # 保存成功后回到循环顶部,刷新账号信息页面

        elif choice == "2":
            break


def main() -> None:
    while True:
        _clear_screen()
        console.print(_build_menu_panel())
        console.print()
        choice = console.input("[bold]> [/bold]").strip()

        if choice == "1":
            _handle_login()
        elif choice == "2":
            _handle_config()
        elif choice == "3":
            _clear_screen()
            console.print(
                Panel(
                    "[bold]再见！[/bold]",
                    border_style="cyan",
                    width=PANEL_WIDTH,
                )
            )
            break
        else:
            console.print("[bold red]无效选项，请重新输入。[/bold red]")


if __name__ == "__main__":
    main()

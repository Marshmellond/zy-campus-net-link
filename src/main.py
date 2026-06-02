"""
程序入口模块
交互式菜单，双击 exe 即可使用
"""

import os
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import config
import network

console = Console()
PANEL_WIDTH = 56

MAX_RETRIES = 6
RETRY_INTERVAL = 10


def _clear_screen() -> None:
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


def _key_pressed() -> bool:
    """非阻塞检测是否有按键输入"""
    if sys.platform == "win32":
        import msvcrt
        return msvcrt.kbhit()
    else:
        import select
        return select.select([sys.stdin], [], [], 0)[0] != []


def _flush_input() -> None:
    """清空输入缓冲区"""
    if sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()


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

        elif choice == "2":
            break


def _auto_login() -> None:
    """自动登录模式：重试 6 次，每次间隔 10 秒，中途可按回车切手动模式"""
    account = config.get_account()

    _clear_screen()

    header = Text()
    header.append("正在自动连接校园网...\n", style="bold yellow")
    header.append("按 ", style="dim")
    header.append("回车键", style="bold white")
    header.append(" 切换到手动操作", style="dim")

    console.print(
        Panel(header, title="自动模式", border_style="yellow", width=PANEL_WIDTH, padding=(1, 3))
    )

    for attempt in range(1, MAX_RETRIES + 1):
        console.print(f"\n[bold yellow][{attempt}/{MAX_RETRIES}][/bold yellow] 连接中...", end="")

        result = network.login(account["username"], account["password"])

        if result["ok"]:
            console.print(f"\n[bold green]✓ {result['message']}[/bold green]")
            console.print()
            console.print(
                Panel(
                    "[bold green]连接成功！3 秒后自动关闭...[/bold green]",
                    border_style="green",
                    width=PANEL_WIDTH,
                )
            )

            # 等 3 秒，同时检测回车
            _flush_input()
            for _ in range(30):
                if _key_pressed():
                    _flush_input()
                    break
                time.sleep(0.1)
            sys.exit(0)

        console.print(f"\r[bold red][{attempt}/{MAX_RETRIES}][/bold red] ✗ 连接失败: {result['message']}")

        if attempt == MAX_RETRIES:
            break

        # 等 10 秒，每 0.5 秒检查一次是否按了回车
        for _ in range(RETRY_INTERVAL * 2):
            if _key_pressed():
                _flush_input()
                console.print()
                console.print()
                console.input("[dim]已切换到手动模式，按回车键进入菜单...[/dim]")
                return
            time.sleep(0.5)

    # 6 次全部失败
    console.print()
    console.print()
    console.print(
        Panel(
            "[bold red]6 次重试均失败，请检查账号密码是否正确。[/bold red]",
            border_style="red",
            width=PANEL_WIDTH,
        )
    )
    console.print()
    console.input("[dim]按回车键进入主菜单...[/dim]")


def main() -> None:
    account = config.get_account()

    # 首次使用（没有账号）→ 直接进手动菜单
    if account["username"] and account["password"]:
        _auto_login()

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

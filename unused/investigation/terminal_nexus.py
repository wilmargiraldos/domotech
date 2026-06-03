"""
TerminalNexus - TUI estilo cyberpunk usando Rich
Instalar dependencias: pip install rich pyfiglet
"""

import time
import random
from datetime import datetime
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.table import Table
from rich.console import Console
from rich import box

try:
    import pyfiglet
    FIGLET_AVAILABLE = True
except ImportError:
    FIGLET_AVAILABLE = False

console = Console()

# ─── Configuración ───────────────────────────────────────────────
TARGET = "Late Night Bugfixing Beats – Deep Focus Coding Music for 2AM Debug Sessions"
VERSION = "v1.0.0-alpha"

RESPUESTAS = [
    "Signal acquired. Your node is now active.",
    "Access granted. Welcome to the mainframe.",
    "Authorized entity recognized. Enjoy the stream.",
    "Login detected. Connection secure.",
    "Data packet decoded. Thank you for the input.",
    "Neural link established. Stream synced.",
    "Identity verified. Encryption key loaded.",
]

# ─── Estado global ───────────────────────────────────────────────
chat_messages = []
uptime_seconds = 0
progress_val = 0

# ─── Helpers ─────────────────────────────────────────────────────

def make_title() -> Text:
    """Título ASCII art con colores neon."""
    if FIGLET_AVAILABLE:
        ascii_art = pyfiglet.figlet_format("TerminalNexus", font="banner3-D")
    else:
        ascii_art = "  ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     \n"
        ascii_art += "  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     \n"
        ascii_art += "     ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     \n"
        ascii_art += "     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     \n"
        ascii_art += "     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗\n"
        ascii_art += "     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝\n"
        ascii_art += "                         N E X U S"

    t = Text()
    colors = ["magenta", "bright_magenta", "purple", "bright_magenta", "magenta"]
    lines = ascii_art.splitlines()
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        t.append(line + "\n", style=f"bold {color}")
    return t


def format_uptime(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def make_system_panel(uptime: int, progress: float) -> Panel:
    """Panel de estado del sistema con barra de progreso."""
    # Barra de progreso manual
    bar_width = 40
    filled = int(bar_width * progress / 100)
    bar = Text()
    bar.append("Progress: ", style="white")
    bar.append("█" * filled, style="bright_blue")
    bar.append("░" * (bar_width - filled), style="dim blue")
    bar.append(f"  {progress:.0f}%", style="cyan")

    status_line = Text()
    status_line.append(f"Uptime: {format_uptime(uptime)}", style="green")
    status_line.append("    Status: ", style="white")
    status_line.append("WAITING FOR VIEWER, COMMENT, LIKE, SHARE & SUBSCRIBE...", style="bright_cyan")

    table = Table.grid(padding=(0, 2))
    table.add_row(Text("[EXECUTING BACKGROUND PROCESS]", style="bold white"), bar)
    table.add_row(status_line)

    return Panel(
        table,
        title="[bold white]SYSTEM EXECUTION[/bold white]",
        border_style="bright_white",
        box=box.SQUARE,
    )


def make_chat_panel(messages: list) -> Panel:
    """Panel de chat en vivo estilo terminal."""
    content = Text()

    # Encabezado de instrucción
    content.append(
        "  [SYSTEM REQ]: Drop a message in the ",
        style="bright_red"
    )
    content.append("live chat", style="bold white")
    content.append("! Your ", style="bright_red")
    content.append("NAME", style="bold white")
    content.append(" will be displayed in 29 minutes.\n\n", style="bright_red")

    # Mensajes
    for ts, user, msg in messages[-8:]:  # Últimos 8 mensajes
        content.append(f"  > [{ts}] ", style="white")
        content.append("[ROOT\\]", style="bold red")
        content.append(" -> Guest ", style="white")
        content.append(f"[@{user}\\]", style="bold white")
        content.append(f": {msg}\n", style="bright_cyan")

    return Panel(
        content,
        border_style="bright_red",
        box=box.SQUARE,
        padding=(0, 0),
    )


def make_streaming_panel() -> Panel:
    """Panel de streams en vivo."""
    t = Text()
    t.append("  [Waiting for other live streams...]\n", style="white")
    return Panel(
        t,
        title="[bold bright_magenta]\\[STREAMING CLUSTER STATUS]: OTHER LIVE STREAMS[/bold bright_magenta]",
        border_style="bright_magenta",
        box=box.SQUARE,
    )


def make_footer() -> Text:
    """Barra inferior con métricas del sistema."""
    cpu = random.uniform(30, 65)
    ram = random.uniform(10, 25)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    t = Text(justify="center")
    t.append(f"  CPU: {cpu:.1f}%", style="green")
    t.append(" | ", style="dim white")
    t.append(f"RAM: {ram:.1f}%", style="green")
    t.append(" | ", style="dim white")
    t.append("GPU: N/A", style="green")
    t.append(" | ", style="dim white")
    t.append(f"UTC: {now}", style="green")
    t.append("  \n", style="white")
    return t


def make_header() -> Text:
    """Línea de versión y target."""
    t = Text()
    t.append(f"  {VERSION}", style="bold white")
    t.append(" | ", style="dim white")
    t.append("TARGET: ", style="bold white")
    t.append(TARGET + "\n", style="bright_green")
    return t


def generate_layout(uptime: int, progress: float, messages: list) -> Layout:
    """Ensambla el layout completo."""
    layout = Layout()
    layout.split_column(
        Layout(name="title", size=10),
        Layout(name="header", size=3),
        Layout(name="system", size=6),
        Layout(name="chat", size=14),
        Layout(name="streaming", size=5),
        Layout(name="footer", size=2),
    )

    layout["title"].update(
        Panel(make_title(), border_style="bright_magenta", box=box.SQUARE)
    )
    layout["header"].update(
        Panel(make_header(), border_style="bright_white", box=box.SQUARE)
    )
    layout["system"].update(make_system_panel(uptime, progress))
    layout["chat"].update(make_chat_panel(messages))
    layout["streaming"].update(make_streaming_panel())
    layout["footer"].update(make_footer())

    return layout


# ─── Simulación de chat ──────────────────────────────────────────

FAKE_USERS = [
    "sadhitler_888", "fguitton", "vrmaroli", "sildeman",
    "justinlow4170", "WilmarGiraldo", "x0_coder", "NightOwlDev",
    "loop_master", "synthwave_fan",
]


def simulate_chat_message(messages: list):
    """Agrega un mensaje simulado al chat."""
    ts = datetime.utcnow().strftime("%y%m%d %H:%M:%S")
    user = random.choice(FAKE_USERS)
    msg = random.choice(RESPUESTAS)
    messages.append((ts, user, msg))


# ─── Main ─────────────────────────────────────────────────────────

def main():
    global uptime_seconds, progress_val, chat_messages

    # Mensajes iniciales
    for _ in range(4):
        simulate_chat_message(chat_messages)

    console.clear()

    with Live(
        generate_layout(uptime_seconds, progress_val, chat_messages),
        refresh_per_second=2,
        screen=True,
    ) as live:
        try:
            while True:
                uptime_seconds += 1
                progress_val = min(100, progress_val + random.uniform(0.05, 0.2))
                if progress_val >= 100:
                    progress_val = 0

                # Nuevo mensaje cada ~5 segundos
                if uptime_seconds % 5 == 0:
                    simulate_chat_message(chat_messages)

                live.update(
                    generate_layout(uptime_seconds, progress_val, chat_messages)
                )
                time.sleep(0.5)

        except KeyboardInterrupt:
            console.print("\n[bold red]  [CONNECTION TERMINATED BY USER][/bold red]\n")


if __name__ == "__main__":
    main()

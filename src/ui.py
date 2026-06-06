"""
Interface CLI estilo Claude Code — Mission Control AI | EnviroSat.

Usa Rich para renderização de painéis e prompt-toolkit para input editável.
Comandos disponíveis: /help, /status, /about, /clear, /exit
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

console = Console()

# Estilo do prompt de input
session = PromptSession(
    style=Style.from_dict({"prompt": "#06B6D4 bold"})
)

# Cor tema do EnviroSat — verde para sustentabilidade
COR_TEMA = "#22C55E"
COR_ALERTA = "#EF4444"
COR_INFO = "#06B6D4"


def show_banner():
    """Exibe banner ASCII colorido e card de boas-vindas."""
    # Linha 1 — Global Solution
    linha1 = pyfiglet.figlet_format("EnviroSat", font="slant")
    # Linha 2 — Mission Control AI
    linha2 = pyfiglet.figlet_format("Mission Control", font="small")

    console.print(Text(linha1, style=f"bold {COR_TEMA}"))
    console.print(Text(linha2, style=f"bold {COR_INFO}"))
    console.print(
        Text(
            "── 2026.1 · Prompt Engineering and AI · FIAP · Trilha: Observação Ambiental ──",
            style="italic #8484A0",
        )
    )
    console.print()
    console.print(
        Panel.fit(
            "[bold]Sistema de monitoramento de satélite ambiental com IA generativa.[/bold]\n"
            "Detecta focos de incêndio, desmatamento e anomalias orbitais em tempo real.\n\n"
            f"Modelo: [bold {COR_INFO}]gpt-oss:120b[/bold {COR_INFO}] via Ollama Cloud\n"
            "Digite [bold]/help[/bold] para ver os comandos disponíveis.",
            title=f"[bold {COR_TEMA}]🌳 MISSION CONTROL — ENVIROSAT[/bold {COR_TEMA}]",
            border_style=COR_TEMA,
        )
    )
    console.print()


def show_response(text: str):
    """Renderiza resposta da IA em painel com timestamp."""
    agora = datetime.now().strftime("%H:%M:%S")
    console.print(
        Panel(
            text,
            title=f"[bold {COR_TEMA}]🌳 EnviroSat AI[/bold {COR_TEMA}]",
            subtitle=f"[dim]{agora}[/dim]",
            border_style=COR_TEMA,
        )
    )
    console.print()


def show_help():
    """Exibe tabela de comandos disponíveis."""
    tabela = Table(
        title="Comandos disponíveis",
        border_style=COR_INFO,
        show_header=True,
        header_style=f"bold {COR_INFO}",
    )
    tabela.add_column("Comando", style="bold")
    tabela.add_column("Descrição")

    tabela.add_row("/status",  "Exibe snapshot atual da telemetria e alertas ativos")
    tabela.add_row("/about",   "Informações sobre o projeto e a trilha EnviroSat")
    tabela.add_row("/help",    "Mostra este menu de ajuda")
    tabela.add_row("/clear",   "Limpa a tela e exibe o banner novamente")
    tabela.add_row("/exit",    "Encerra a Mission Control AI")
    tabela.add_row("[qualquer texto]", "Envia pergunta para análise da IA com base na telemetria atual")

    console.print(tabela)
    console.print()


def show_about():
    """Exibe informações sobre o projeto."""
    texto = (
        "[bold]🌳 EnviroSat — Observação Ambiental[/bold]\n\n"
        "Satélite simulado baseado em missões como Amazônia-1 e Landsat.\n"
        "Monitora sensores de detecção de focos de incêndio e desmatamento.\n\n"
        "[bold]Parâmetros monitorados:[/bold]\n"
        "  🌡  Sensor térmico — temperatura indicativa de focos ativos\n"
        "   Sensor óptico  — integridade para análise de cobertura vegetal\n"
        "   Buffer          — ocupação da memória de imagens a bordo\n"
        "   Geolocalização  — precisão das coordenadas dos focos detectados\n"
        "   Energia         — carga dos painéis solares\n\n"
        "[bold]Personas atendidas:[/bold]\n"
        "  • Operador de centro de controle ambiental (INPE / órgão estadual)\n"
        "  • Coordenador de brigada de combate a incêndio\n"
        "  • Analista de compliance ambiental\n\n"
        "[bold]Stack técnica:[/bold] Python 3.10+ · Ollama Cloud (gpt-oss:120b) · Rich · prompt-toolkit\n\n"
        "[bold]FIAP[/bold] · Ciência da Computação · Global Solution 2026.1\n"
        "Disciplina: Prompt Engineering and Artificial Intelligence"
    )
    console.print(Panel(texto, title="[bold]ℹ️  Sobre o projeto[/bold]", border_style=COR_INFO))
    console.print()


def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()

    # Aviso se a engine ainda não estiver pronta
    if not engine.is_ready():
        console.print(
            "  ⚠  Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n",
            style="yellow",
        )

    while True:
        try:
            user_input = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Encerrando Mission Control AI...[/dim]")
            break

        if not user_input:
            continue

        # ── Comandos especiais ────────────────────────────────────────────────
        if user_input.lower() == "/exit":
            console.print("[dim]Missão encerrada. Até a próxima órbita.[/dim]")
            break

        if user_input.lower() == "/help":
            show_help()
            continue

        if user_input.lower() == "/about":
            show_about()
            continue

        if user_input.lower() == "/clear":
            console.clear()
            show_banner()
            continue

        if user_input.lower() == "/status":
            with console.status("[bold green]Coletando telemetria...[/bold green]"):
                snapshot = engine.status_snapshot()
            show_response(snapshot)
            continue

        # ── Análise da IA ─────────────────────────────────────────────────────
        with console.status("[bold green]Analisando com IA...[/bold green]"):
            resposta = engine.analyze(user_input)

        show_response(resposta)

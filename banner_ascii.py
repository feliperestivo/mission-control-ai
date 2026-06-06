"""
banner_ascii.py — Gerador de banner ASCII para Mission Control AI.

Uso:
  python banner_ascii.py                         # Banner padrão
  python banner_ascii.py -fonts                  # Lista fontes disponíveis
  python banner_ascii.py -font slant -text "Oi"  # Testa fonte específica
  python banner_ascii.py -demo                   # Mostra 8 fontes lado a lado
"""

import sys
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

console = Console()


def banner_padrao():
    """Exibe o banner padrão do projeto."""
    linha1 = pyfiglet.figlet_format("EnviroSat", font="slant")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="small")

    console.print(Align.center(Text(linha1, style="bold #22C55E")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(
        Align.center(
            Text(
                "── 2026.1 · Prompt Engineering and AI · FIAP ──",
                style="italic #8484A0",
            )
        )
    )


def listar_fontes():
    """Lista todas as fontes disponíveis no PyFiglet."""
    fontes = pyfiglet.FigletFont.getFonts()
    console.print(f"\n[bold]Total de fontes disponíveis:[/bold] {len(fontes)}\n")
    for i, fonte in enumerate(sorted(fontes)):
        console.print(f"  {i+1:3d}. {fonte}")


def testar_fonte(font: str, texto: str):
    """Testa uma fonte específica com um texto."""
    try:
        resultado = pyfiglet.figlet_format(texto, font=font)
        console.print(Panel(resultado, title=f"Fonte: {font}", border_style="#06B6D4"))
    except pyfiglet.FontNotFound:
        console.print(f"[red]Fonte '{font}' não encontrada.[/red]")


def demo_fontes():
    """Mostra 8 fontes diferentes lado a lado."""
    fontes_demo = ["slant", "small", "banner", "digital", "doom", "lean", "mini", "standard"]
    texto_demo = "EnviroSat"
    for fonte in fontes_demo:
        try:
            resultado = pyfiglet.figlet_format(texto_demo, font=fonte)
            console.print(Panel(resultado, title=f"[bold]{fonte}[/bold]", border_style="#22C55E"))
        except Exception:
            console.print(f"[dim]Fonte {fonte} indisponível[/dim]")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        banner_padrao()
    elif "-fonts" in args:
        listar_fontes()
    elif "-demo" in args:
        demo_fontes()
    elif "-font" in args:
        try:
            idx_font = args.index("-font")
            font_nome = args[idx_font + 1]
            texto = "Mission Control AI"
            if "-text" in args:
                idx_text = args.index("-text")
                texto = args[idx_text + 1]
            testar_fonte(font_nome, texto)
        except (IndexError, ValueError):
            console.print("[red]Uso: python banner_ascii.py -font <nome_da_fonte> [-text 'texto'][/red]")
    else:
        banner_padrao()

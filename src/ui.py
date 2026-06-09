"""Interface CLI visual para Mission Control AI — EnviroSat."""

from datetime import datetime

import pyfiglet
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def show_banner():
    """Exibe banner inicial."""
    console.clear()

    banner = pyfiglet.figlet_format("EnviroSat", font="slant")
    console.print(Align.center(Text(banner, style="bold #06B6D4")))

    subtitulo = Text(
        "Mission Control AI • FIAP Global Solution 2026.1",
        style="bold #A855F7"
    )
    console.print(Align.center(subtitulo))

    console.print()

    console.print(Panel.fit(
        "🛰️ Sistema de monitoramento orbital com IA generativa\n"
        "🌎 Trilha: EnviroSat — Sustentabilidade e clima\n"
        "🤖 Modelo: gpt-oss:120b via Ollama Cloud\n\n"
        "Digite uma pergunta ou use /help para ver os comandos.",
        title="◆ CENTRAL DE CONTROLE",
        border_style="#06B6D4",
        padding=(1, 4)
    ))


def show_help():
    """Mostra comandos disponíveis e sugestões de simulação."""
    table = Table(
        title="Comandos disponíveis",
        border_style="#06B6D4",
        show_header=True,
        header_style="bold #A855F7"
    )

    table.add_column("Comando", style="bold #06B6D4")
    table.add_column("Função", style="white")

    table.add_row("/help", "Mostra esta lista de comandos")
    table.add_row("/status", "Gera um ciclo de telemetria atual")
    table.add_row("/about", "Explica o objetivo do projeto")
    table.add_row("/clear", "Limpa a tela e mostra o banner novamente")
    table.add_row("/exit", "Encerra o sistema")

    console.print(table)

    simulacoes = (
        "Experimente digitar:\n\n"
        "🔥 simule incêndio na Amazônia Legal\n"
        "🔋 simule energia baixa\n"
        "📡 simule falha de comunicação\n"
        "🟢 status normal\n"
        "🛰️ como está a missão?"
    )

    console.print(Panel(
        simulacoes,
        title="◆ Sugestões de simulação",
        border_style="green",
        padding=(1, 2)
    ))

def show_response(text):
    """Renderiza a resposta em painel."""
    now = datetime.now().strftime("%H:%M")

    border_style = "#06B6D4"

    if "CRÍTICA" in text:
        border_style = "red"
    elif "ATENÇÃO" in text:
        border_style = "yellow"
    elif "NOMINAL" in text:
        border_style = "green"

    console.print()
    console.print(Panel(
        text,
        title="🛰️ Mission Control",
        subtitle=f"Análise gerada às {now}",
        border_style=border_style,
        padding=(1, 2)
    ))
    console.print()


def show_about():
    """Mostra descrição do projeto."""
    texto = (
        "🚀 Mission Control AI — EnviroSat\n\n"
        "Este sistema simula a telemetria de um satélite de observação ambiental.\n"
        "A lógica Python avalia os dados, gera alertas e dispara respostas automáticas.\n\n"
        "Depois disso, a IA generativa interpreta o cenário em linguagem natural, "
        "conectando cada anomalia orbital ao impacto terrestre, como combate a queimadas, "
        "monitoramento de áreas protegidas e apoio a brigadas ambientais."
    )

    console.print(Panel(
        texto,
        title="◆ Sobre o projeto",
        border_style="#A855F7",
        padding=(1, 2)
    ))


def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()

    if not engine.is_ready():
        console.print(
            "⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n",
            style="bold yellow"
        )
    else:
        console.print("✅ Engine status: OPERACIONAL\n", style="bold green")

    while True:
        try:
            user_input = input("🛰️ EnviroSat ❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        if user_input == "/exit":
            console.print("\nEncerrando Mission Control AI... 👋", style="bold #06B6D4")
            break

        if user_input == "/help":
            show_help()
            continue

        if user_input == "/about":
            show_about()
            continue

        if user_input == "/status":
            resposta = engine.status_snapshot()
            show_response(resposta)
            continue

        if user_input == "/clear":
            show_banner()
            continue

        resposta = engine.analyze(user_input)
        show_response(resposta)
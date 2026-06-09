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

    banner = pyfiglet.figlet_format("ENVIROSAT", font="ansi_shadow")
    console.print(Align.center(Text(banner, style="bold #06B6D4")))

    console.print(Align.center(Text(
        "MISSION CONTROL AI · FIAP GLOBAL SOLUTION 2026.1",
        style="bold #A855F7"
    )))

    console.print(Align.center(Text(
        "Observação ambiental · Telemetria simulada · IA generativa",
        style="italic #94A3B8"
    )))

    console.print()

    painel = (
        "🛰️  Satélite simulado: EnviroSat\n"
        "🌎  Missão: monitorar áreas ambientais sensíveis\n"
        "🤖  IA: gpt-oss:120b via Ollama Cloud\n"
        "⚙️  Lógica: Python + thresholds + respostas automáticas\n\n"
        "Digite uma pergunta ou use [bold cyan]/help[/bold cyan] para ver comandos e simulações."
    )

    console.print(Panel.fit(
        painel,
        title="◆ CENTRAL DE CONTROLE OPERACIONAL",
        subtitle="sistema online",
        border_style="#06B6D4",
        padding=(1, 4)
    ))


def show_help():
    """Mostra comandos disponíveis e sugestões de simulação."""
    comandos = Table(
        title="📟 Comandos da CLI",
        border_style="#06B6D4",
        show_header=True,
        header_style="bold #A855F7"
    )

    comandos.add_column("Comando", style="bold #06B6D4", no_wrap=True)
    comandos.add_column("Descrição", style="white")

    comandos.add_row("/help", "Mostra comandos e sugestões de simulação")
    comandos.add_row("/status", "Gera um ciclo aleatório de telemetria")
    comandos.add_row("/about", "Explica a proposta do projeto")
    comandos.add_row("/clear", "Limpa a tela e recarrega o painel inicial")
    comandos.add_row("/exit", "Encerra a central de controle")

    console.print(comandos)

    simulacoes = Table(
        title="🧪 Cenários prontos para simulação",
        border_style="green",
        show_header=True,
        header_style="bold green"
    )

    simulacoes.add_column("Cenário", style="bold")
    simulacoes.add_column("Digite no terminal", style="white")
    simulacoes.add_column("O que demonstra", style="#CBD5E1")

    simulacoes.add_row(
        "🔥 Incêndio",
        "simule incêndio na Amazônia Legal",
        "Sensor térmico alto, focos detectados e alerta crítico"
    )
    simulacoes.add_row(
        "🔋 Energia baixa",
        "simule energia baixa",
        "Ativação de modo economia e preservação do payload"
    )
    simulacoes.add_row(
        "📡 Comunicação",
        "simule falha de comunicação",
        "Downlink degradado e priorização de imagens críticas"
    )
    simulacoes.add_row(
        "🟢 Operação normal",
        "status normal",
        "Parâmetros dentro dos limites esperados"
    )
    simulacoes.add_row(
        "🛰️ Consulta livre",
        "como está a missão?",
        "Análise operacional completa via IA"
    )

    console.print()
    console.print(simulacoes)


def show_response(text):
    """Renderiza a resposta em painel com cor conforme severidade."""
    now = datetime.now().strftime("%H:%M")

    border_style = "#06B6D4"
    titulo_status = "🛰️ Mission Control"

    if "CRÍTICA" in text:
        border_style = "red"
        titulo_status = "🔴 ALERTA CRÍTICO"
    elif "ATENÇÃO" in text:
        border_style = "yellow"
        titulo_status = "🟡 ATENÇÃO OPERACIONAL"
    elif "NOMINAL" in text:
        border_style = "green"
        titulo_status = "🟢 MISSÃO NOMINAL"

    console.print()
    console.print(Panel(
        text,
        title=titulo_status,
        subtitle=f"análise gerada às {now}",
        border_style=border_style,
        padding=(1, 2)
    ))
    console.print()


def show_about():
    """Mostra descrição do projeto."""
    texto = (
        "[bold cyan]Mission Control AI — EnviroSat[/bold cyan]\n\n"
        "Este projeto simula uma central de controle para um satélite de observação ambiental.\n\n"
        "O sistema gera telemetria simulada, avalia os dados por regras Python, identifica "
        "anomalias e aciona respostas automáticas. Em seguida, a IA generativa interpreta "
        "a missão em linguagem natural e conecta o problema técnico ao impacto terrestre.\n\n"
        "[bold]Impactos analisados:[/bold]\n"
        "• Combate a queimadas\n"
        "• Monitoramento de áreas protegidas\n"
        "• Apoio a brigadas ambientais\n"
        "• Priorização de imagens críticas para tomada de decisão"
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
        console.print("⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n", style="bold yellow")
    else:
        console.print("✅ Engine status: OPERACIONAL\n", style="bold green")

    while True:
        try:
            user_input = input("🛰️ EnviroSat Control ❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        comando = user_input.lower()

        if comando == "/exit":
            console.print("\nEncerrando Mission Control AI... 👋", style="bold #06B6D4")
            break

        if comando == "/help":
            show_help()
            continue

        if comando == "/about":
            show_about()
            continue

        if comando == "/status":
            resposta = engine.status_snapshot()
            show_response(resposta)
            continue

        if comando == "/clear":
            show_banner()
            continue

        resposta = engine.analyze(user_input)
        show_response(resposta)
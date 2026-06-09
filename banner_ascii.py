import argparse

import pyfiglet
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def render(text="ENVIROSAT\nMISSION CONTROL AI", font="ansi_shadow"):
    console.clear()

    for line in text.split("\n"):
        ascii_text = pyfiglet.figlet_format(line, font=font)
        console.print(Align.center(Text(ascii_text, style="bold #06B6D4")))

    console.print(Align.center(Text(
        "FIAP · Global Solution 2026.1 · Prompt Engineering and Artificial Intelligence",
        style="bold #A855F7"
    )))

    console.print()
    console.print(Panel.fit(
        "🛰️ Observação ambiental orbital\n"
        "🌎 Sustentabilidade, queimadas e áreas protegidas\n"
        "🤖 Análise operacional com IA generativa",
        title="◆ ENVIROSAT",
        border_style="#06B6D4",
        padding=(1, 4)
    ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-font", default="ansi_shadow")
    parser.add_argument("-text", default="ENVIROSAT\nMISSION CONTROL AI")
    parser.add_argument("-fonts", action="store_true")
    parser.add_argument("-demo", action="store_true")

    args = parser.parse_args()

    if args.fonts:
        print("\n".join(pyfiglet.FigletFont.getFonts()))
    elif args.demo:
        for font in ["ansi_shadow", "slant", "doom", "big", "standard", "isometric1"]:
            console.rule(font)
            render(args.text, font)
    else:
        render(args.text, args.font)
"""Motor de análise da Mission Control AI."""

import os
from pathlib import Path
from dotenv import load_dotenv
from ollama import Client
from src.telemetria import coletar
from src.alertas import avaliar

load_dotenv()

TRILHA = "envirosat"

client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY', '')}
)


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []

    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        return client.chat(
            model="gpt-oss:120b", messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md."""
    path = Path("prompts/system_prompt.md")

    if path.exists():
        return path.read_text(encoding="utf-8")

    return "Você é um assistente."


class MissionEngine:
    """Motor de análise — vocês completam os métodos abaixo."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()

    def is_ready(self):
        return True

    def status_snapshot(self):
        """Retorna texto resumindo o estado atual da telemetria."""
        dados = coletar()
        diagnostico = avaliar(dados)

        return self._formatar_status(dados, diagnostico)

    def analyze(self, pergunta_usuario):
        """Analisa a pergunta com base na telemetria + alertas + IA."""
        texto = pergunta_usuario.lower()

        if "incêndio" in texto or "incendio" in texto or "queimada" in texto or "fogo" in texto:
            dados = coletar("incendio")

        elif "energia" in texto or "bateria" in texto:
            dados = coletar("energia_baixa")

        elif "comunicação" in texto or "comunicacao" in texto or "downlink" in texto or "sinal" in texto or "buffer" in texto:
            dados = coletar("comunicacao")

        elif "normal" in texto or "nominal" in texto or "estável" in texto or "estavel" in texto:
            dados = coletar("normal")

        else:
            dados = coletar()

        diagnostico = avaliar(dados)

        prompt = f"""
Pergunta do operador:
{pergunta_usuario}

Telemetria atual do EnviroSat:
{dados}

Diagnóstico gerado por regras Python:
{diagnostico}

Gere uma análise operacional em português brasileiro.
Explique:
1. O estado técnico da missão.
2. Os alertas detectados.
3. As respostas automatizadas tomadas pelo sistema.
4. O impacto terrestre para monitoramento ambiental, queimadas e áreas protegidas.
""".strip()

        resposta_ia = llm(prompt, system=self.system_prompt)

        status_formatado = self._formatar_status(dados, diagnostico)
        return status_formatado + "\n\n" + resposta_ia

    def _formatar_status(self, dados, diagnostico):
        alertas = "\n".join(f"- {a}" for a in diagnostico["alertas"])
        acoes = "\n".join(f"- {a}" for a in diagnostico["acoes_automaticas"])

        return f""" ENVIROSAT / MISSION CONTROL AI
Status: {diagnostico["severidade"]}
Cenário simulado: {dados["cenario"]}
Área monitorada: {dados["area_monitorada"]}
Timestamp: {dados["timestamp"]}

Telemetria:
- Sensor térmico: {dados["sensor_termico_c"]} °C
- Sensor óptico RGB+NIR: {dados["sensor_optico_percent"]}%
- Buffer de imagens: {dados["buffer_imagens_percent"]}%
- Precisão de geolocalização: {dados["precisao_geolocalizacao_m"]} m
- Energia disponível: {dados["energia_percent"]}%
- Sinal de downlink: {dados["sinal_downlink_percent"]}%
- Focos detectados: {dados["focos_detectados"]}

Alertas Python:
{alertas if alertas else "- Nenhum alerta crítico."}

Respostas automatizadas:
{acoes if acoes else "- Nenhuma ação automática necessária."}"""
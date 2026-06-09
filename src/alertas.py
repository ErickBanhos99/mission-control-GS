"""Regras de threshold e respostas automatizadas para EnviroSat."""


def avaliar(dados):
    alertas = []
    acoes = []
    severidade = "NOMINAL"

    if dados["sensor_termico_c"] >= 70 or dados["focos_detectados"] >= 10:
        alertas.append(
            "Risco alto de incêndio/desmatamento: assinatura térmica e focos acima do esperado."
        )
        acoes.append(
            "Priorizar captura térmica da área e enviar alerta para brigada ambiental."
        )
        severidade = "CRÍTICA"

    elif dados["sensor_termico_c"] >= 60 or dados["focos_detectados"] >= 5:
        alertas.append("🌡 Atenção térmica: possível início de foco de calor.")
        acoes.append(
            "Aumentar frequência de monitoramento sobre a área nos próximos ciclos."
        )
        severidade = max_sev(severidade, "ATENÇÃO")

    if dados["energia_percent"] < 20:
        alertas.append(" Energia crítica: risco de perda operacional do payload ambiental.")
        acoes.append(
            "Ativar modo economia: reduzir coletas não essenciais e preservar downlink prioritário."
        )
        severidade = "CRÍTICA"

    elif dados["energia_percent"] < 35:
        alertas.append(" Energia baixa: operação deve ser controlada.")
        acoes.append("Agendar recarga e limitar uso do sensor óptico até estabilização.")
        severidade = max_sev(severidade, "ATENÇÃO")

    if dados["sinal_downlink_percent"] < 40 or dados["buffer_imagens_percent"] > 85:
        alertas.append(
            "Comunicação degradada: risco de atraso no envio de imagens ambientais."
        )
        acoes.append(
            "Compactar pacotes, priorizar imagens críticas e tentar nova janela de downlink."
        )
        severidade = max_sev(severidade, "ATENÇÃO")

    if dados["precisao_geolocalizacao_m"] > 15:
        alertas.append(
            "Geolocalização imprecisa: coordenadas podem dificultar resposta em campo."
        )
        acoes.append(
            "Recalibrar posição e cruzar dados com sensores ópticos antes de acionar equipes."
        )
        severidade = max_sev(severidade, "ATENÇÃO")

    if not alertas:
        alertas.append("Operação nominal: parâmetros dentro dos limites esperados.")
        acoes.append(
            "Manter monitoramento padrão e registrar ciclo como referência operacional."
        )

    return {
        "severidade": severidade,
        "alertas": alertas,
        "acoes_automaticas": acoes
    }


def max_sev(atual, nova):
    ordem = {
        "NOMINAL": 0,
        "ATENÇÃO": 1,
        "CRÍTICA": 2
    }

    return nova if ordem[nova] > ordem[atual] else atual
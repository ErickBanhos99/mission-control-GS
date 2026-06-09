"""Geração de telemetria simulada para a trilha EnviroSat."""

import random
from datetime import datetime

CENARIOS = {
    "normal": {
        "sensor_termico_c": (38, 50),
        "sensor_optico_percent": (86, 100),
        "buffer_imagens_percent": (20, 55),
        "precisao_geolocalizacao_m": (3, 9),
        "energia_percent": (60, 100),
        "sinal_downlink_percent": (75, 100),
        "focos_detectados": (0, 2),
    },
    "incendio": {
        "sensor_termico_c": (68, 88),
        "sensor_optico_percent": (65, 90),
        "buffer_imagens_percent": (55, 95),
        "precisao_geolocalizacao_m": (8, 22),
        "energia_percent": (35, 75),
        "sinal_downlink_percent": (50, 90),
        "focos_detectados": (8, 34),
    },
    "energia_baixa": {
        "sensor_termico_c": (42, 58),
        "sensor_optico_percent": (72, 95),
        "buffer_imagens_percent": (30, 70),
        "precisao_geolocalizacao_m": (4, 13),
        "energia_percent": (8, 24),
        "sinal_downlink_percent": (45, 85),
        "focos_detectados": (1, 8),
    },
    "comunicacao": {
        "sensor_termico_c": (40, 62),
        "sensor_optico_percent": (70, 95),
        "buffer_imagens_percent": (82, 100),
        "precisao_geolocalizacao_m": (7, 18),
        "energia_percent": (45, 85),
        "sinal_downlink_percent": (5, 35),
        "focos_detectados": (2, 14),
    },
}

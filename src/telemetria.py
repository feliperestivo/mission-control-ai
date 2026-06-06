"""
Módulo de telemetria simulada — Trilha EnviroSat.

Simula os dados de um satélite de observação ambiental (similar ao Amazônia-1 / Landsat)
monitorando focos de incêndio, desmatamento e integridade do sensor.

Parâmetros monitorados:
  - sensor_termico      : temperatura do sensor térmico (°C) — detecta focos de calor
  - sensor_optico       : integridade do sensor óptico RGB+NIR (%)
  - buffer_imagens      : buffer de imagens não transmitidas (%)
  - precisao_geoloc     : precisão de geolocalização (metros de erro)
  - energia_disponivel  : carga da bateria solar (%)
"""

import random
from datetime import datetime


# Faixas de operação normal para cada parâmetro
RANGES_NORMAIS = {
    "sensor_termico":      (10.0,  55.0),   # °C — acima de 55 °C indica possível foco
    "sensor_optico":       (80.0, 100.0),   # % — abaixo de 80 % indica degradação
    "buffer_imagens":      (0.0,   70.0),   # % — acima de 70 % risco de perda de dados
    "precisao_geoloc":     (0.0,   15.0),   # m — acima de 15 m compromete localização
    "energia_disponivel":  (20.0, 100.0),   # % — abaixo de 20 % entra modo economia
}

# Ciclo interno do satélite para simular variação temporal
_ciclo = 0


def coletar() -> dict:
    """
    Gera uma leitura simulada de telemetria do EnviroSat.
    Os valores variam levemente a cada chamada, simulando ciclos orbitais.

    Retorna:
        dict com os 5 parâmetros monitorados + timestamp.
    """
    global _ciclo
    _ciclo += 1

    # Geração dos valores com pequena variação aleatória por ciclo
    dados = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ciclo_orbital": _ciclo,

        # Sensor térmico — tende a subir no hemisfério iluminado
        "sensor_termico": round(
            random.uniform(18.0, 62.0) + (_ciclo % 5) * 1.2, 1
        ),

        # Sensor óptico — degrada lentamente ao longo dos ciclos
        "sensor_optico": round(
            max(55.0, random.uniform(72.0, 100.0) - (_ciclo % 10) * 0.8), 1
        ),

        # Buffer de imagens — sobe com o tempo, reset após downlink
        "buffer_imagens": round(
            min(100.0, random.uniform(10.0, 50.0) + (_ciclo % 8) * 4.5), 1
        ),

        # Precisão de geolocalização — varia com interferências ionosféricas
        "precisao_geoloc": round(
            random.uniform(2.0, 22.0), 1
        ),

        # Energia disponível — ciclo solar (sobe/desce conforme órbita)
        "energia_disponivel": round(
            max(5.0, min(100.0, 60.0 + 35.0 * abs((_ciclo % 10) / 5.0 - 1.0) + random.uniform(-8.0, 8.0))), 1
        ),
    }

    return dados


def formatar_leitura(dados: dict) -> str:
    """Formata os dados de telemetria em texto legível para o terminal."""
    linhas = [
        f"   Timestamp       : {dados['timestamp']}",
        f"   Ciclo orbital   : #{dados['ciclo_orbital']}",
        f"   Sensor térmico  : {dados['sensor_termico']} °C",
        f"   Sensor óptico   : {dados['sensor_optico']} %",
        f"   Buffer imagens  : {dados['buffer_imagens']} %",
        f"   Precisão geoloc : {dados['precisao_geoloc']} m",
        f"   Energia disp.   : {dados['energia_disponivel']} %",
    ]
    return "\n".join(linhas)

"""
Módulo de alertas e decisão — Trilha EnviroSat.

Contém toda a lógica de threshold implementada em Python puro.
A IA não decide o que é crítico — o código decide.
A IA interpreta e contextualiza para o operador.
"""

# ── Thresholds de alerta ──────────────────────────────────────────────────────

THRESHOLDS = {
    # Sensor térmico: acima de 55 °C indica possível foco de incêndio ativo
    "sensor_termico_critico":    55.0,   # °C
    "sensor_termico_atencao":    45.0,   # °C

    # Sensor óptico: abaixo de 80 % compromete qualidade das imagens
    "sensor_optico_critico":     65.0,   # %
    "sensor_optico_atencao":     80.0,   # %

    # Buffer de imagens: acima de 80 % risco real de perda de dados
    "buffer_critico":            85.0,   # %
    "buffer_atencao":            70.0,   # %

    # Precisão de geolocalização: acima de 15 m compromete localização de focos
    "geoloc_critico":            20.0,   # m
    "geoloc_atencao":            15.0,   # m

    # Energia: abaixo de 20 % ativa modo economia de energia
    "energia_critica":           15.0,   # %
    "energia_atencao":           20.0,   # %
}

# Níveis de severidade
NIVEL_OK       = "✅ NORMAL"
NIVEL_ATENCAO  = "⚠️  ATENÇÃO"
NIVEL_CRITICO  = "🔴 CRÍTICO"


def avaliar(dados: dict) -> list[dict]:
    """
    Avalia os dados de telemetria e retorna lista de alertas detectados.

    Cada alerta tem:
        - parametro  : nome do parâmetro
        - valor      : valor atual
        - nivel      : OK / ATENÇÃO / CRÍTICO
        - mensagem   : descrição curta do problema
        - impacto    : o que isso significa para o operador / brigada
        - acao_auto  : ação automática tomada pelo sistema (se houver)
    """
    alertas = []

    # ── 1. Sensor térmico ────────────────────────────────────────────────────
    temp = dados["sensor_termico"]
    if temp > THRESHOLDS["sensor_termico_critico"]:
        alertas.append({
            "parametro": "sensor_termico",
            "valor": f"{temp} °C",
            "nivel": NIVEL_CRITICO,
            "mensagem": "Temperatura do sensor acima de 55 °C — possível foco de incêndio detectado.",
            "impacto": "Brigadas ambientais e IBAMA precisam ser notificados imediatamente. "
                       "Risco de propagação para áreas protegidas.",
            "acao_auto": "🚨 ALERTA AUTOMÁTICO: Imagem priorizando área crítica para próximo downlink.",
        })
    elif temp > THRESHOLDS["sensor_termico_atencao"]:
        alertas.append({
            "parametro": "sensor_termico",
            "valor": f"{temp} °C",
            "nivel": NIVEL_ATENCAO,
            "mensagem": "Temperatura do sensor elevada — monitorar próximas leituras.",
            "impacto": "Possível início de aquecimento em área de vegetação seca.",
            "acao_auto": None,
        })

    # ── 2. Sensor óptico ─────────────────────────────────────────────────────
    optico = dados["sensor_optico"]
    if optico < THRESHOLDS["sensor_optico_critico"]:
        alertas.append({
            "parametro": "sensor_optico",
            "valor": f"{optico} %",
            "nivel": NIVEL_CRITICO,
            "mensagem": "Sensor óptico com integridade crítica — imagens comprometidas.",
            "impacto": "Dados de desmatamento e cobertura vegetal podem ser inválidos. "
                       "Relatórios DETER/PRODES afetados.",
            "acao_auto": "🔧 AÇÃO AUTOMÁTICA: Iniciando sequência de recalibração do sensor.",
        })
    elif optico < THRESHOLDS["sensor_optico_atencao"]:
        alertas.append({
            "parametro": "sensor_optico",
            "valor": f"{optico} %",
            "nivel": NIVEL_ATENCAO,
            "mensagem": "Sensor óptico com degradação leve — qualidade de imagem reduzida.",
            "impacto": "Análise de desmatamento pode ter menor precisão.",
            "acao_auto": None,
        })

    # ── 3. Buffer de imagens ─────────────────────────────────────────────────
    buffer = dados["buffer_imagens"]
    if buffer > THRESHOLDS["buffer_critico"]:
        alertas.append({
            "parametro": "buffer_imagens",
            "valor": f"{buffer} %",
            "nivel": NIVEL_CRITICO,
            "mensagem": "Buffer de imagens quase cheio — risco de perda de dados.",
            "impacto": "Imagens de áreas críticas podem ser sobrescritas antes do downlink.",
            "acao_auto": "📡 AÇÃO AUTOMÁTICA: Downlink emergencial solicitado para próxima janela disponível.",
        })
    elif buffer > THRESHOLDS["buffer_atencao"]:
        alertas.append({
            "parametro": "buffer_imagens",
            "valor": f"{buffer} %",
            "nivel": NIVEL_ATENCAO,
            "mensagem": "Buffer de imagens em 70 % — monitorar ocupação.",
            "impacto": "Atenção ao agendamento do próximo downlink.",
            "acao_auto": None,
        })

    # ── 4. Precisão de geolocalização ────────────────────────────────────────
    geoloc = dados["precisao_geoloc"]
    if geoloc > THRESHOLDS["geoloc_critico"]:
        alertas.append({
            "parametro": "precisao_geoloc",
            "valor": f"{geoloc} m",
            "nivel": NIVEL_CRITICO,
            "mensagem": "Erro de geolocalização acima de 20 m — localização de focos comprometida.",
            "impacto": "Brigadas podem ser enviadas para coordenadas incorretas. "
                       "Risco operacional direto.",
            "acao_auto": "🛰  AÇÃO AUTOMÁTICA: Sincronização forçada com satélites de referência GNSS.",
        })
    elif geoloc > THRESHOLDS["geoloc_atencao"]:
        alertas.append({
            "parametro": "precisao_geoloc",
            "valor": f"{geoloc} m",
            "nivel": NIVEL_ATENCAO,
            "mensagem": "Precisão de geolocalização levemente degradada.",
            "impacto": "Pequena margem de erro nas coordenadas de focos detectados.",
            "acao_auto": None,
        })

    # ── 5. Energia disponível ────────────────────────────────────────────────
    energia = dados["energia_disponivel"]
    if energia < THRESHOLDS["energia_critica"]:
        alertas.append({
            "parametro": "energia_disponivel",
            "valor": f"{energia} %",
            "nivel": NIVEL_CRITICO,
            "mensagem": "Nível crítico de energia — risco de desligamento.",
            "impacto": "Satélite pode perder capacidade de captura. "
                       "Monitoramento ambiental interrompido.",
            "acao_auto": "⚡ AÇÃO AUTOMÁTICA: Modo economia ativado. Sensores não essenciais suspensos.",
        })
    elif energia < THRESHOLDS["energia_atencao"]:
        alertas.append({
            "parametro": "energia_disponivel",
            "valor": f"{energia} %",
            "nivel": NIVEL_ATENCAO,
            "mensagem": "Energia abaixo de 20 % — monitorar carga solar.",
            "impacto": "Redução de capacidade operacional nas próximas horas.",
            "acao_auto": "⚡ AÇÃO AUTOMÁTICA: Modo economia de energia ativado preventivamente.",
        })

    return alertas


def resumo_status(dados: dict, alertas: list) -> str:
    """Retorna um resumo textual do estado geral da missão."""
    criticos = [a for a in alertas if "CRÍTICO" in a["nivel"]]
    atencao  = [a for a in alertas if "ATENÇÃO" in a["nivel"]]

    if criticos:
        return f"🔴 MISSÃO EM ESTADO CRÍTICO — {len(criticos)} alerta(s) crítico(s) ativo(s)."
    elif atencao:
        return f"⚠️  MISSÃO COM ALERTAS — {len(atencao)} parâmetro(s) em atenção."
    else:
        return "✅ MISSÃO NOMINAL — todos os parâmetros dentro do esperado."

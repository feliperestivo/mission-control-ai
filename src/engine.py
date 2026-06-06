"""
Motor de análise — Mission Control AI | Trilha EnviroSat.

Combina dados de telemetria, lógica de alertas e IA generativa
para gerar análises contextualizadas em linguagem natural.
"""

import os
from pathlib import Path
from ollama import Client
from dotenv import load_dotenv

from src.telemetria import coletar, formatar_leitura
from src.alertas import avaliar, resumo_status

load_dotenv()

# Identificação da trilha
TRILHA = "envirosat"

# Cliente Ollama Cloud
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")}
)


def llm(prompt: str, system: str = None, max_tokens: int = 800, temperature: float = 0.3) -> str:
    """
    Envia prompt ao modelo gpt-oss:120b via Ollama Cloud e retorna o texto gerado.

    Args:
        prompt      : mensagem do usuário
        system      : system prompt (opcional)
        max_tokens  : limite de tokens na resposta
        temperature : criatividade do modelo (0 = mais determinístico)

    Returns:
        Texto da resposta ou mensagem de erro.
    """
    mensagens = []
    if system:
        mensagens.append({"role": "system", "content": system})
    mensagens.append({"role": "user", "content": prompt})

    try:
        resposta = client.chat(
            model="gpt-oss:120b",
            messages=mensagens,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )
        return resposta["message"]["content"].strip()
    except Exception as e:
        return f"⚠️  Erro ao consultar IA: {e}"


def carregar_system_prompt() -> str:
    """Lê o system prompt do arquivo prompts/system_prompt.md."""
    caminho = Path("prompts/system_prompt.md")
    if caminho.exists():
        return caminho.read_text(encoding="utf-8")
    # Fallback simples caso o arquivo não seja encontrado
    return (
        "Você é um sistema de monitoramento de satélite ambiental. "
        "Analise os dados de telemetria e forneça análises claras em português."
    )


def montar_prompt_analise(dados: dict, alertas: list, pergunta: str) -> str:
    """
    

    
    """
    # Formata os alertas em texto
    if alertas:
        alertas_txt = "\n".join([
            f"  [{a['nivel']}] {a['parametro'].upper()}: {a['mensagem']}\n"
            f"  Impacto terrestre: {a['impacto']}\n"
            f"  Ação automática: {a['acao_auto'] if a['acao_auto'] else 'Nenhuma ação automática tomada.'}"
            for a in alertas
        ])
    else:
        alertas_txt = "  Nenhum alerta ativo. Todos os parâmetros dentro do normal."

    prompt = f"""
=== LEITURA DE TELEMETRIA — ENVIROSAT ===

Dados coletados:
{formatar_leitura(dados)}

=== ALERTAS DETECTADOS PELO SISTEMA ===
{alertas_txt}

=== PERGUNTA DO OPERADOR ===
{pergunta}

=== INSTRUÇÕES PARA ANÁLISE ===
Responda em português brasileiro. Seja direto e objetivo.
Sempre conecte a análise técnica ao impacto terrestre (brigadas, IBAMA, produtores, comunidades).
Priorize informações acionáveis — o operador precisa saber o que fazer agora.
"""
    return prompt


class MissionEngine:
    """Motor central da Mission Control AI — conecta telemetria, alertas e IA."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = carregar_system_prompt()
        self._historico = []  # memória das últimas leituras (diferencial)

    def is_ready(self) -> bool:
        """Indica se o motor está pronto para análise."""
        return True

    def status_snapshot(self) -> str:
        """Retorna um snapshot do estado atual da missão em texto formatado."""
        dados = coletar()
        alertas = avaliar(dados)
        status = resumo_status(dados, alertas)

        linhas = [
            f"\n{status}\n",
            "─── Leitura atual de telemetria ───────────────────────",
            formatar_leitura(dados),
            "",
        ]

        if alertas:
            linhas.append("─── Alertas ativos ────────────────────────────────────")
            for a in alertas:
                linhas.append(f"  {a['nivel']} | {a['parametro'].upper()}: {a['mensagem']}")
                if a["acao_auto"]:
                    linhas.append(f"    → {a['acao_auto']}")
        else:
            linhas.append("─── Sem alertas ativos ────────────────────────────────")
            linhas.append("  Todos os sistemas operando normalmente.")

        return "\n".join(linhas)

    def analyze(self, pergunta_usuario: str) -> str:
        """
        
        
            
        
            
            
            
        """
        # 1. Coletar dados reais simulados
        dados = coletar()

        # 2. Avaliar alertas via lógica Python
        alertas = avaliar(dados)

        # 3. Guardar na memória de contexto (diferencial: histórico)
        self._historico.append({
            "ciclo": dados["ciclo_orbital"],
            "status": resumo_status(dados, alertas),
            "n_alertas": len(alertas),
        })
        # Mantém apenas os últimos 5 ciclos no histórico
        if len(self._historico) > 5:
            self._historico.pop(0)

        # Adiciona contexto histórico ao prompt se disponível
        historico_txt = ""
        if len(self._historico) > 1:
            historico_txt = "\n=== HISTÓRICO DOS ÚLTIMOS CICLOS ===\n"
            for h in self._historico[:-1]:
                historico_txt += f"  Ciclo #{h['ciclo']}: {h['status']} ({h['n_alertas']} alerta(s))\n"

        # 4. Montar prompt e chamar IA
        prompt_base = montar_prompt_analise(dados, alertas, pergunta_usuario)
        prompt_completo = historico_txt + prompt_base

        resposta = llm(prompt_completo, system=self.system_prompt)

        return resposta

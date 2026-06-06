"""Mission Control AI — ponto de entrada do sistema.

Trilha: EnviroSat — Observação Ambiental
Disciplina: Prompt Engineering and Artificial Intelligence — FIAP 2026.1
"""

from src.ui import run_cli
from src.engine import MissionEngine

if __name__ == "__main__":
    engine = MissionEngine()
    run_cli(engine)

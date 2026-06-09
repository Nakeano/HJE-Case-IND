
from datetime import datetime, timedelta
from copy import deepcopy

# ---------------------------------------------------------------------------
# Banco de dados em memória (mock)
# Estrutura espelha o que viria de uma tabela `usuarios` + `medicoes`
# ---------------------------------------------------------------------------

_AGORA = datetime.now()

def _dt(horas_atras: float) -> str:
    """Helper para gerar timestamps relativos ao momento atual."""
    return (_AGORA - timedelta(hours=horas_atras)).strftime("%Y-%m-%dT%H:%M:%S")


usuarios_db: dict[int, dict] = {        # usuario_id -> dados do usuário e última medição relevante
    1: {
        "id": 1,
        "nome": "Ana Beatriz Santos",
        "ultima_medicao": _dt(0.3),
        "resultado": "Normal",
        "tempo_decorrido_min": 18,
        "acompanhamento_registrado": False,
    },
    2: {
        "id": 2,
        "nome": "Carlos Eduardo Melo",
        "ultima_medicao": _dt(26),        # >24h sem acompanhamento → destaque urgência
        "resultado": "Irregular",
        "tempo_decorrido_min": 1560,
        "acompanhamento_registrado": False,
    },
    3: {
        "id": 3,
        "nome": "Fernanda Lima",
        "ultima_medicao": _dt(1.5),
        "resultado": "Normal",
        "tempo_decorrido_min": 90,
        "acompanhamento_registrado": False,
    },
    4: {
        "id": 4,
        "nome": "Roberto Alves",
        "ultima_medicao": _dt(30),        # >24h, irregular, sem acompanhamento
        "resultado": "Irregular",
        "tempo_decorrido_min": 1800,
        "acompanhamento_registrado": False,
    },
    5: {
        "id": 5,
        "nome": "Patrícia Nunes",
        "ultima_medicao": _dt(3),
        "resultado": "Irregular",
        "tempo_decorrido_min": 180,
        "acompanhamento_registrado": True,   # já revisado — não exibe urgência
    },
    6: {
        "id": 6,
        "nome": "Marcos Vinícius Costa",
        "ultima_medicao": _dt(0.1),
        "resultado": "Normal",
        "tempo_decorrido_min": 6,
        "acompanhamento_registrado": False,
    },
    7: {
        "id": 7,
        "nome": "Juliana Ferreira",
        "ultima_medicao": _dt(999),       # Nunca completou medição
        "resultado": "Sem dados",
        "tempo_decorrido_min": None,
        "acompanhamento_registrado": False,
    },
    8: {
        "id": 8,
        "nome": "Diego Souza",
        "ultima_medicao": _dt(48),
        "resultado": "Irregular",
        "tempo_decorrido_min": 2880,
        "acompanhamento_registrado": False,
    },
}

# ---------------------------------------------------------------------------
# Histórico de medições por usuário (mock)
# ---------------------------------------------------------------------------

_historico_db: dict[int, list[dict]] = {                #  usuario_id -> lista de medições
    1: [
        {"timestamp": _dt(0.3),  "bpm": 72,  "resultado": "Normal",    "confianca": 0.97},
        {"timestamp": _dt(24.3), "bpm": 68,  "resultado": "Normal",    "confianca": 0.95},
        {"timestamp": _dt(48.3), "bpm": 74,  "resultado": "Normal",    "confianca": 0.98},
    ],
    2: [
        {"timestamp": _dt(26),   "bpm": 140, "resultado": "Irregular", "confianca": 0.61},
        {"timestamp": _dt(50),   "bpm": 88,  "resultado": "Normal",    "confianca": 0.92},
        {"timestamp": _dt(74),   "bpm": 135, "resultado": "Irregular", "confianca": 0.58},
    ],
    3: [
        {"timestamp": _dt(1.5),  "bpm": 65,  "resultado": "Normal",    "confianca": 0.99},
    ],
    4: [
        {"timestamp": _dt(30),   "bpm": 155, "resultado": "Irregular", "confianca": 0.54},
        {"timestamp": _dt(54),   "bpm": 148, "resultado": "Irregular", "confianca": 0.52},
    ],
    5: [
        {"timestamp": _dt(3),    "bpm": 130, "resultado": "Irregular", "confianca": 0.72},
        {"timestamp": _dt(27),   "bpm": 70,  "resultado": "Normal",    "confianca": 0.96},
    ],
    6: [
        {"timestamp": _dt(0.1),  "bpm": 58,  "resultado": "Normal",    "confianca": 0.98},
    ],
    7: [],
    8: [
        {"timestamp": _dt(48),   "bpm": 162, "resultado": "Irregular", "confianca": 0.49},
        {"timestamp": _dt(72),   "bpm": 158, "resultado": "Irregular", "confianca": 0.51},
        {"timestamp": _dt(96),   "bpm": 145, "resultado": "Irregular", "confianca": 0.55},
    ],
}

# Log de acompanhamentos registrados (auditoria)
_log_acompanhamentos: list[dict] = []


# ---------------------------------------------------------------------------
# Funções de acesso (interface pública desta camada)
# ---------------------------------------------------------------------------

def get_historico(usuario_id: int) -> list[dict]:
    """Retorna cópia do histórico para evitar mutação acidental."""
    return deepcopy(_historico_db.get(usuario_id, []))


def registrar_acompanhamento(usuario_id: int, operador: str) -> None:
    """
    Marca o usuário como revisado e grava no log de auditoria.
    O log é relevante para compliance LGPD/ANS: demonstra que
    alertas foram efetivamente tratados pela equipe clínica.
    """
    usuarios_db[usuario_id]["acompanhamento_registrado"] = True

    _log_acompanhamentos.append({
        "usuario_id": usuario_id,
        "operador": operador,
        "timestamp": datetime.now().isoformat(),
    })
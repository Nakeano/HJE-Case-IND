"""
  - app.py        : configuração, rotas e tratamento de erros HTTP
  - data.py       : camada de dados (mock) — isolada para facilitar
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from data import usuarios_db, registrar_acompanhamento, get_historico

app = Flask(__name__)

# CORS habilitado para que o frontend estático possa consumir a API
CORS(app)

def _usuario_payload(u: dict) -> dict:
    """
    Serializa um usuário para o formato esperado pelo frontend.
    Centralizado aqui para evitar duplicação entre rotas.
    """
    return {
        "id": u["id"],
        "nome": u["nome"],
        "ultima_medicao": u["ultima_medicao"],
        "resultado": u["resultado"],
        "tempo_decorrido_min": u["tempo_decorrido_min"],
        "acompanhamento_registrado": u["acompanhamento_registrado"],
    }

# Rotas

@app.get("/usuarios")
def listar_usuarios():
    """
    Retorna lista de todos os usuários com dados de monitoramento.
    """
    filtro = request.args.get("resultado", "").lower()

    resultado = [
        _usuario_payload(u)
        for u in usuarios_db.values()
        if not filtro or u["resultado"].lower() == filtro
    ]

    return jsonify(resultado), 200


@app.get("/usuarios/<int:usuario_id>")
def detalhe_usuario(usuario_id: int):
    """
    Retorna dados + histórico de medições de um usuário específico.
    Retorna 404 se o ID não existir
    """
    usuario = usuarios_db.get(usuario_id)
    if not usuario:
        return jsonify({"erro": f"Usuário {usuario_id} não encontrado"}), 404

    return jsonify({
        **_usuario_payload(usuario),
        "historico": get_historico(usuario_id),
    }), 200


@app.post("/usuarios/<int:usuario_id>/acompanhamento")
def registrar_revisao(usuario_id: int):
    """
    Registra que um operador revisou o caso de um usuário.
    Marca o campo acompanhamento_registrado=True, removendo o
    destaque vermelho de urgência no frontend.
    """
    usuario = usuarios_db.get(usuario_id)
    if not usuario:
        return jsonify({"erro": f"Usuário {usuario_id} não encontrado"}), 404

    # Impede registros de acompanhamento em casos que não geraram alerta —
    # mantém integridade do log de revisões para fins de auditoria (LGPD/ANS)
    if usuario["resultado"] != "Irregular":
        return jsonify({
            "erro": "Acompanhamento só pode ser registrado para resultados Irregulares"
        }), 422

    operador = request.json.get("operador") if request.is_json else None
    if not operador or not isinstance(operador, str) or not operador.strip():
        return jsonify({"erro": "Campo 'operador' obrigatório no corpo JSON"}), 400

    registrar_acompanhamento(usuario_id, operador.strip())

    return jsonify({
        "mensagem": "Acompanhamento registrado com sucesso",
        "usuario_id": usuario_id,
        "operador": operador.strip(),
        "timestamp": datetime.now().isoformat(),
    }), 200

if __name__ == "__main__":
    # debug=False em produção — nunca expor stack traces ao cliente
    app.run(host="0.0.0.0", port=5000, debug=True)
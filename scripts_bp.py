from flask import Blueprint, jsonify, request, current_app
from scripts.cadastro_pessoas import cadastrar_pessoa
from scripts.gerar_slots import gerar_slots_a_partir_excel
from scripts.bloquear_slots import bloquear_slot, reverter_bloqueio_slot
from scripts.adicionar_link_meet import adicionar_link_meet
import os

scripts_bp = Blueprint("scripts", __name__)

@scripts_bp.route("/scripts/cadastrar_pessoa", methods=["POST"])
def run_cadastrar_pessoa():
    data = request.json
    result = cadastrar_pessoa(
        app=current_app,
        nome=data["nome"],
        email=data["email"],
        cpf=data["cpf"],
        telefone=data["telefone"],
        idade=data["idade"],
        tipo=data["tipo"],
        funcao_admin=data.get("funcao_admin"),
        especialidade=data.get("especialidade"),
        crm=data.get("crm"),
        unidade=data.get("unidade"),
        disponibilidade=data.get("disponibilidade"),
        family_id=data.get("family_id"),
    )
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Erro ao cadastrar pessoa"}), 400

@scripts_bp.route("/scripts/gerar_slots", methods=["POST"])
def run_gerar_slots():
    data = request.json
    excel_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", data.get("excel_path", "OSZO_MVP_Final_Exemplo.xlsx")))
    sheet_name = data.get("sheet_name", "Agenda_Profissional")
    data_inicio_geracao_str = data.get("data_inicio_geracao")
    num_semanas = data.get("num_semanas", 4)

    data_inicio_geracao = None
    if data_inicio_geracao_str:
        from datetime import date
        data_inicio_geracao = date.fromisoformat(data_inicio_geracao_str)

    try:
        gerar_slots_a_partir_excel(app=current_app, excel_path=excel_file, sheet_name=sheet_name, data_inicio_geracao=data_inicio_geracao, num_semanas=num_semanas)
        return jsonify({"message": "Slots gerados com sucesso!"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao gerar slots: {str(e)}"}), 400

@scripts_bp.route("/scripts/bloquear_slot", methods=["POST"])
def run_bloquear_slot():
    data = request.json
    consulta_id = data.get("consulta_id")
    if bloquear_slot(app=current_app, consulta_id=consulta_id):
        return jsonify({"message": f"Slot para consulta {consulta_id} bloqueado com sucesso!"}), 200
    return jsonify({"message": f"Erro ao bloquear slot para consulta {consulta_id}"}), 400

@scripts_bp.route("/scripts/reverter_bloqueio_slot", methods=["POST"])
def run_reverter_bloqueio_slot():
    data = request.json
    consulta_id = data.get("consulta_id")
    if reverter_bloqueio_slot(app=current_app, consulta_id=consulta_id):
        return jsonify({"message": f"Bloqueio de slot para consulta {consulta_id} revertido com sucesso!"}), 200
    return jsonify({"message": f"Erro ao reverter bloqueio de slot para consulta {consulta_id}"}), 400

@scripts_bp.route("/scripts/adicionar_link_meet", methods=["POST"])
def run_adicionar_link_meet():
    data = request.json
    consulta_id = data.get("consulta_id")
    link_meet = data.get("link_meet")
    if adicionar_link_meet(app=current_app, consulta_id=consulta_id, link_meet=link_meet):
        return jsonify({"message": f"Link Meet adicionado à consulta {consulta_id} com sucesso!"}), 200
    return jsonify({"message": f"Erro ao adicionar Link Meet à consulta {consulta_id}"}), 400



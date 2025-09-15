
import os
import sys
from datetime import datetime

# Adiciona o diretório pai ao sys.path para que os módulos possam ser encontrados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import db
from src.models.consulta import Consulta
from src.models.medico import HorarioDisponivel

def bloquear_slot(app, consulta_id):
    with app.app_context():
        consulta = Consulta.query.get(consulta_id)
        if not consulta:
            print(f"Consulta com ID {consulta_id} não encontrada.")
            return False

        if consulta.slot_id:
            slot = HorarioDisponivel.query.get(consulta.slot_id)
            if slot:
                if consulta.status == "agendada" or consulta.status == "confirmada":
                    slot.disponivel = False
                    slot.paciente_id = consulta.paciente_id # Adicionar paciente_id ao slot se necessário
                    slot.consulta_id = consulta.id # Adicionar consulta_id ao slot se necessário
                    db.session.commit()
                    print(f"Slot {slot.id} bloqueado para a consulta {consulta.id}.")
                    return True
                elif consulta.status == "cancelada":
                    slot.disponivel = True
                    slot.paciente_id = None
                    slot.consulta_id = None
                    db.session.commit()
                    print(f"Slot {slot.id} liberado devido ao cancelamento da consulta {consulta.id}.")
                    return True
            else:
                print(f"Slot com ID {consulta.slot_id} não encontrado.")
        else:
            print(f"Consulta {consulta.id} não possui um slot associado.")
        return False

def reverter_bloqueio_slot(app, consulta_id):
    with app.app_context():
        consulta = Consulta.query.get(consulta_id)
        if not consulta:
            print(f"Consulta com ID {consulta_id} não encontrada.")
            return False

        if consulta.slot_id:
            slot = HorarioDisponivel.query.get(consulta.slot_id)
            if slot:
                slot.disponivel = True
                slot.paciente_id = None
                slot.consulta_id = None
                db.session.commit()
                print(f"Slot {slot.id} liberado para a consulta {consulta.id}.")
                return True
            else:
                print(f"Slot com ID {consulta.slot_id} não encontrado.")
        else:
            print(f"Consulta {consulta.id} não possui um slot associado.")
        return False

if __name__ == "__main__":
    print("Este script deve ser chamado via API.")



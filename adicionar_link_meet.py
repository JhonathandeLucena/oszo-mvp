
import os
import sys

# Adiciona o diretório pai ao sys.path para que os módulos possam ser encontrados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import db
from src.models.consulta import Consulta

def adicionar_link_meet(app, consulta_id, link_meet):
    with app.app_context():
        consulta = Consulta.query.get(consulta_id)
        if not consulta:
            print(f"Consulta com ID {consulta_id} não encontrada.")
            return False

        if consulta.type == "online":
            consulta.link_meet = link_meet
            db.session.commit()
            print(f"Link Meet {link_meet} adicionado à consulta online {consulta_id}.")
            return True
        else:
            print(f"Consulta {consulta_id} não é do tipo online. Link Meet não adicionado.")
            return False

if __name__ == "__main__":
    print("Este script deve ser chamado via API.")




import os
import sys
from datetime import datetime

# Adiciona o diretório pai ao sys.path para que os módulos possam ser encontrados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import db
from src.models.user import User
from src.models.medico import Medico

def cadastrar_pessoa(app, nome, email, cpf, telefone, idade, tipo, funcao_admin=None, especialidade=None, crm=None, unidade=None, disponibilidade=None, family_id=None):
    with app.app_context():
        if tipo == "Paciente" or (tipo == "Colaborador" and funcao_admin == "admin"):
            # Cadastrar como User
            user_type = "administrador" if funcao_admin == "admin" else "paciente"
            user = User(
                name=nome,
                email=email,
                cpf=cpf,
                telefone=telefone,
                idade=idade,
                family_id=family_id,
                password="senha_padrao", # Senha padrão, deve ser alterada
                user_type=user_type
            )
            db.session.add(user)
            db.session.commit()
            print(f"Usuário {nome} ({user_type}) cadastrado com sucesso!")
            return user.to_dict()
        elif tipo == "Profissional":
            # Cadastrar como Medico
            medico = Medico(
                name=nome,
                email=email, # Adicionar email ao modelo Medico se não existir
                cpf=cpf,     # Adicionar cpf ao modelo Medico se não existir
                telefone=telefone,
                specialty=especialidade,
                crm=crm,
                unidade=unidade,
                disponibilidade=disponibilidade,
                rating=0.0, # Valor padrão
                price=0.0   # Valor padrão
            )
            db.session.add(medico)
            db.session.commit()
            print(f"Profissional {nome} ({especialidade}) cadastrado com sucesso!")
            return medico.to_dict()
        else:
            print(f"Tipo de pessoa {tipo} não suportado para cadastro.")
            return None

if __name__ == "__main__":
    # Este bloco não será executado diretamente, pois os scripts serão chamados via blueprint
    print("Este script deve ser chamado via API.")



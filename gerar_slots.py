
import os
import sys
from datetime import datetime, timedelta, date, time
import pandas as pd

# Adiciona o diretório pai ao sys.path para que os módulos possam ser encontrados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import db
from src.models.medico import Medico, HorarioDisponivel

def gerar_slots_para_profissional(app, profissional_id, dia_semana, inicio_str, fim_str, tipo_atendimento, data_inicio_geracao, num_semanas=4):
    with app.app_context():
        medico = Medico.query.filter_by(id=profissional_id).first()
        if not medico:
            print(f"Médico com ID {profissional_id} não encontrado.")
            return

        dias_da_semana = {
            "Segunda": 0, "Terça": 1, "Quarta": 2, "Quinta": 3, "Sexta": 4, "Sábado": 5, "Domingo": 6
        }
        dia_semana_int = dias_da_semana.get(dia_semana)
        if dia_semana_int is None:
            print(f"Dia da semana inválido: {dia_semana}")
            return

        inicio_hora = datetime.strptime(inicio_str, "%H:%M").time()
        fim_hora = datetime.strptime(fim_str, "%H:%M").time()

        current_date = data_inicio_geracao
        while current_date.weekday() != dia_semana_int:
            current_date += timedelta(days=1)

        for _ in range(num_semanas):
            if current_date.weekday() == dia_semana_int:
                hora_atual = datetime.combine(current_date, inicio_hora)
                while hora_atual.time() < fim_hora:
                    hora_fim_slot = (hora_atual + timedelta(minutes=30)).time()
                    if hora_fim_slot > fim_hora:
                        break

                    # Verificar se o slot já existe para evitar duplicatas
                    existing_slot = HorarioDisponivel.query.filter_by(
                        medico_id=medico.id,
                        data=current_date,
                        hora_inicio=hora_atual.time(),
                        tipo_atendimento=tipo_atendimento
                    ).first()

                    if not existing_slot:
                        slot = HorarioDisponivel(
                            medico_id=medico.id,
                            data=current_date,
                            hora_inicio=hora_atual.time(),
                            hora_fim=hora_fim_slot,
                            disponivel=True,
                            tipo_atendimento=tipo_atendimento
                        )
                        db.session.add(slot)
                        print(f"Slot gerado para {medico.name} em {current_date} das {hora_atual.time()} às {hora_fim_slot} ({tipo_atendimento})")
                    else:
                        print(f"Slot já existe para {medico.name} em {current_date} das {hora_atual.time()} às {hora_fim_slot} ({tipo_atendimento})")

                    hora_atual += timedelta(minutes=30)
            current_date += timedelta(weeks=1)
        db.session.commit()

def gerar_slots_a_partir_excel(app, excel_path, sheet_name="Agenda_Profissional", data_inicio_geracao=None, num_semanas=4):
    if data_inicio_geracao is None:
        data_inicio_geracao = date.today()

    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    for index, row in df.iterrows():
        profissional_id = row["ProfissionalID"]
        dia_semana = row["DiaSemana"]
        inicio = row["Inicio"]
        fim = row["Fim"]
        tipo_atendimento = row["TipoAtendimento"]

        # Converter ProfissionalID de string (P001) para int (1) se necessário
        # Assumindo que o ID do médico no banco de dados é um inteiro auto-incrementado
        # e que P001 corresponde ao id=1, P002 ao id=2, etc.
        # Isso pode precisar de um mapeamento mais robusto em um sistema real
        try:
            medico_db_id = int(profissional_id.replace("P", ""))
        except ValueError:
            print(f"Erro: ProfissionalID inválido no Excel: {profissional_id}")
            continue

        gerar_slots_para_profissional(app, medico_db_id, dia_semana, inicio, fim, tipo_atendimento, data_inicio_geracao, num_semanas)

if __name__ == "__main__":
    print("Este script deve ser chamado via API.")



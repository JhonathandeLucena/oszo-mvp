import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text

# Inicializa o Flask
app = Flask(__name__)
CORS(app)

# Configurações de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")  # Render injeta isso automaticamente
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN", "oszo-12345")

# Conexão com o banco
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ================================
# HEALTH CHECK
# ================================
@app.route("/health")
def health():
    return jsonify({"message": "OSZO backend rodando no Render 🚀", "status": "ok"})


# ================================
# ADMIN - CRIAÇÃO DAS TABELAS
# ================================
@app.route("/api/admin/db/init")
def init_db():
    token = request.args.get("token")
    if token != ADMIN_INIT_TOKEN:
        return jsonify({"error": "Token inválido"}), 403

    try:
        with engine.begin() as conn:
            # Pacientes
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE,
                    criado_em TIMESTAMP DEFAULT NOW()
                )
            """))

            # Profissionais
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS profissionais (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    especialidade TEXT,
                    criado_em TIMESTAMP DEFAULT NOW()
                )
            """))

            # Consultas
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS consultas (
                    id SERIAL PRIMARY KEY,
                    paciente_id INTEGER REFERENCES pacientes(id),
                    profissional_id INTEGER REFERENCES profissionais(id),
                    data TIMESTAMP,
                    status TEXT,
                    criado_em TIMESTAMP DEFAULT NOW()
                )
            """))

        return jsonify({"message": "Tabelas criadas com sucesso!", "status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# CRUD PACIENTES
# ================================
@app.route("/api/pacientes", methods=["GET"])
def listar_pacientes():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM pacientes ORDER BY id"))
        pacientes = [dict(row._mapping) for row in result]
    return jsonify(pacientes)


@app.route("/api/pacientes", methods=["POST"])
def criar_paciente():
    data = request.json
    nome = data.get("nome")
    email = data.get("email")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400

    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO pacientes (nome, email) VALUES (:nome, :email)"),
                {"nome": nome, "email": email}
            )
        return jsonify({"message": "Paciente criado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# CRUD PROFISSIONAIS
# ================================
@app.route("/api/profissionais", methods=["GET"])
def listar_profissionais():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM profissionais ORDER BY id"))
        profissionais = [dict(row._mapping) for row in result]
    return jsonify(profissionais)


@app.route("/api/profissionais", methods=["POST"])
def criar_profissional():
    data = request.json
    nome = data.get("nome")
    especialidade = data.get("especialidade")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400

    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO profissionais (nome, especialidade) VALUES (:nome, :especialidade)"),
                {"nome": nome, "especialidade": especialidade}
            )
        return jsonify({"message": "Profissional criado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# CRUD CONSULTAS
# ================================
@app.route("/api/consultas", methods=["GET"])
def listar_consultas():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT c.id, c.data, c.status,
                   p.nome AS paciente, pr.nome AS profissional, pr.especialidade
            FROM consultas c
            LEFT JOIN pacientes p ON c.paciente_id = p.id
            LEFT JOIN profissionais pr ON c.profissional_id = pr.id
            ORDER BY c.id
        """))
        consultas = [dict(row._mapping) for row in result]
    return jsonify(consultas)


@app.route("/api/consultas", methods=["POST"])
def criar_consulta():
    data = request.json
    paciente_id = data.get("paciente_id")
    profissional_id = data.get("profissional_id")
    data_consulta = data.get("data")
    status = data.get("status", "agendada")

    if not paciente_id or not profissional_id or not data_consulta:
        return jsonify({"error": "Paciente, Profissional e Data são obrigatórios"}), 400

    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO consultas (paciente_id, profissional_id, data, status)
                    VALUES (:paciente_id, :profissional_id, :data, :status)
                """),
                {
                    "paciente_id": paciente_id,
                    "profissional_id": profissional_id,
                    "data": data_consulta,
                    "status": status
                }
            )
        return jsonify({"message": "Consulta criada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# PONTO DE ENTRADA LOCAL
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

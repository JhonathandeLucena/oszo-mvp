import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text

# Inicializa o Flask
app = Flask(__name__)
CORS(app)

# Configurações de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")  # URL do banco vinda do Render
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN", "oszo-12345")

# Conexão com o banco de dados
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ================================
# ROTAS DE STATUS
# ================================
@app.route("/health")
def health():
    """Verifica se o backend está rodando"""
    return jsonify({"message": "OSZO backend rodando no Render 🚀", "status": "ok"})


@app.route("/api/admin/db/init")
def init_db():
    """Cria as tabelas iniciais do MVP"""
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
@app.route("/api/pacientes", methods=["POST"])
def criar_paciente():
    data = request.json
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text("INSERT INTO pacientes (nome, email) VALUES (:nome, :email) RETURNING id"),
                {"nome": data["nome"], "email": data.get("email")}
            )
            paciente_id = result.scalar()
        return jsonify({"id": paciente_id, "message": "Paciente criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pacientes", methods=["GET"])
def listar_pacientes():
    try:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT id, nome, email, criado_em FROM pacientes ORDER BY id"))
            pacientes = [dict(row._mapping) for row in result]
        return jsonify(pacientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# CRUD PROFISSIONAIS
# ================================
@app.route("/api/profissionais", methods=["POST"])
def criar_profissional():
    data = request.json
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text("INSERT INTO profissionais (nome, especialidade) VALUES (:nome, :especialidade) RETURNING id"),
                {"nome": data["nome"], "especialidade": data.get("especialidade")}
            )
            profissional_id = result.scalar()
        return jsonify({"id": profissional_id, "message": "Profissional criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profissionais", methods=["GET"])
def listar_profissionais():
    try:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT id, nome, especialidade, criado_em FROM profissionais ORDER BY id"))
            profissionais = [dict(row._mapping) for row in result]
        return jsonify(profissionais)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# CRUD CONSULTAS
# ================================
@app.route("/api/consultas", methods=["POST"])
def criar_consulta():
    data = request.json
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO consultas (paciente_id, profissional_id, data, status)
                    VALUES (:paciente_id, :profissional_id, :data, :status)
                    RETURNING id
                """),
                {
                    "paciente_id": data["paciente_id"],
                    "profissional_id": data["profissional_id"],
                    "data": data.get("data"),
                    "status": data.get("status", "agendada"),
                }
            )
            consulta_id = result.scalar()
        return jsonify({"id": consulta_id, "message": "Consulta criada com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/consultas", methods=["GET"])
def listar_consultas():
    try:
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT c.id, p.nome AS paciente, pr.nome AS profissional, c.data, c.status, c.criado_em
                FROM consultas c
                JOIN pacientes p ON c.paciente_id = p.id
                JOIN profissionais pr ON c.profissional_id = pr.id
                ORDER BY c.id
            """))
            consultas = [dict(row._mapping) for row in result]
        return jsonify(consultas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# PONTO DE ENTRADA
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

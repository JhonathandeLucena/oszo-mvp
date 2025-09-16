import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text

# ================================
# Inicialização
# ================================
app = Flask(__name__)
CORS(app)

# Configurações de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN", "oszo-12345")

# Conexão com o banco de dados
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ================================
# ROTAS BÁSICAS
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
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE,
                    criado_em TIMESTAMP DEFAULT NOW()
                )
            """))

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS profissionais (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    especialidade TEXT,
                    criado_em TIMESTAMP DEFAULT NOW()
                )
            """))

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
# PACIENTES
# ================================
@app.route("/api/pacientes", methods=["GET"])
def get_pacientes():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, nome, email, criado_em FROM pacientes ORDER BY id"))
            pacientes = [dict(row._mapping) for row in result]
        return jsonify(pacientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pacientes", methods=["POST"])
def create_paciente():
    data = request.json
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO pacientes (nome, email) VALUES (:nome, :email)"),
                {"nome": data["nome"], "email": data.get("email")}
            )
        return jsonify({"message": "Paciente criado com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# PROFISSIONAIS
# ================================
@app.route("/api/profissionais", methods=["GET"])
def get_profissionais():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, nome, especialidade, criado_em FROM profissionais ORDER BY id"))
            profissionais = [dict(row._mapping) for row in result]
        return jsonify(profissionais)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profissionais", methods=["POST"])
def create_profissional():
    data = request.json
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO profissionais (nome, especialidade) VALUES (:nome, :especialidade)"),
                {"nome": data["nome"], "especialidade": data.get("especialidade")}
            )
        return jsonify({"message": "Profissional criado com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# CONSULTAS
# ================================
@app.route("/api/consultas", methods=["GET"])
def get_consultas():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT c.id, c.data, c.status,
                       p.nome AS paciente_nome,
                       pr.nome AS profissional_nome
                FROM consultas c
                LEFT JOIN pacientes p ON c.paciente_id = p.id
                LEFT JOIN profissionais pr ON c.profissional_id = pr.id
                ORDER BY c.id
            """))
            consultas = [dict(row._mapping) for row in result]
        return jsonify(consultas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/consultas", methods=["POST"])
def create_consulta():
    data = request.json
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO consultas (paciente_id, profissional_id, data, status) VALUES (:paciente_id, :profissional_id, :data, :status)"),
                {
                    "paciente_id": data["paciente_id"],
                    "profissional_id": data["profissional_id"],
                    "data": data.get("data"),
                    "status": data.get("status", "agendada")
                }
            )
        return jsonify({"message": "Consulta criada com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# PONTO DE ENTRADA
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


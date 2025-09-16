import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text

# ================================
# Inicialização do app
# ================================
app = Flask(__name__)
CORS(app)

# Configurações de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")  # Definido no Render
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN", "oszo-12345")

# Conexão com o banco de dados
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# ================================
# ROTAS DE SAÚDE E ADMIN
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
# CRUD - PACIENTES
# ================================
@app.route("/api/pacientes", methods=["GET"])
def listar_pacientes():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM pacientes")).mappings().all()
        return jsonify(list(result))


@app.route("/api/pacientes", methods=["POST"])
def criar_paciente():
    data = request.json
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO pacientes (nome, email) VALUES (:nome, :email)"),
            {"nome": data["nome"], "email": data.get("email")},
        )
    return jsonify({"message": "Paciente criado com sucesso!"}), 201


# ================================
# CRUD - PROFISSIONAIS
# ================================
@app.route("/api/profissionais", methods=["GET"])
def listar_profissionais():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM profissionais")).mappings().all()
        return jsonify(list(result))


@app.route("/api/profissionais", methods=["POST"])
def criar_profissional():
    data = request.json
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO profissionais (nome, especialidade) VALUES (:nome, :especialidade)"),
            {"nome": data["nome"], "especialidade": data.get("especialidade")},
        )
    return jsonify({"message": "Profissional criado com sucesso!"}), 201


# ================================
# CRUD - CONSULTAS
# ================================
@app.route("/api/consultas", methods=["GET"])
def listar_consultas():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT c.id, p.nome AS paciente, pr.nome AS profissional, c.data, c.status
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            JOIN profissionais pr ON c.profissional_id = pr.id
        """)).mappings().all()
        return jsonify(list(result))


@app.route("/api/consultas", methods=["POST"])
def criar_consulta():
    data = request.json
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO consultas (paciente_id, profissional_id, data, status)
                VALUES (:paciente_id, :profissional_id, :data, :status)
            """),
            {
                "paciente_id": data["paciente_id"],
                "profissional_id": data["profissional_id"],
                "data": data.get("data"),
                "status": data.get("status", "agendada"),
            },
        )
    return jsonify({"message": "Consulta criada com sucesso!"}), 201


# ================================
# PONTO DE ENTRADA
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text

# ==========================================
# CONFIGURAÇÕES
# ==========================================
app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")  # Render → variável de ambiente
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN", "oszo-12345")

# Conexão com o banco
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# ==========================================
# ROTAS BÁSICAS
# ==========================================
@app.route("/health")
def health():
    return jsonify({"message": "OSZO backend rodando no Render 🚀", "status": "ok"})


@app.route("/api/admin/db/init")
def init_db():
    """Cria tabelas no banco (se não existirem)"""
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
                    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
                    profissional_id INTEGER REFERENCES profissionais(id) ON DELETE CASCADE,
                    data TIMESTAMP,
                    status TEXT,
                    criado_em TIMESTAMP DEFAULT NOW()
                )
            """))

        return jsonify({"message": "Tabelas criadas com sucesso!", "status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# PACIENTES
# ==========================================
@app.route("/api/pacientes", methods=["GET"])
def listar_pacientes():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM pacientes")).mappings().all()
        return jsonify([dict(r) for r in result])


@app.route("/api/pacientes", methods=["POST"])
def criar_paciente():
    data = request.json
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO pacientes (nome, email) VALUES (:nome, :email)"),
            {"nome": data["nome"], "email": data.get("email")}
        )
    return jsonify({"message": "Paciente criado com sucesso"}), 201


@app.route("/api/pacientes/<int:id>", methods=["DELETE"])
def deletar_paciente(id):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM pacientes WHERE id = :id"), {"id": id})
        return jsonify({"message": "Paciente excluído com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# PROFISSIONAIS
# ==========================================
@app.route("/api/profissionais", methods=["GET"])
def listar_profissionais():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM profissionais")).mappings().all()
        return jsonify([dict(r) for r in result])


@app.route("/api/profissionais", methods=["POST"])
def criar_profissional():
    data = request.json
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO profissionais (nome, especialidade) VALUES (:nome, :especialidade)"),
            {"nome": data["nome"], "especialidade": data.get("especialidade")}
        )
    return jsonify({"message": "Profissional criado com sucesso"}), 201


@app.route("/api/profissionais/<int:id>", methods=["DELETE"])
def deletar_profissional(id):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM profissionais WHERE id = :id"), {"id": id})
        return jsonify({"message": "Profissional excluído com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# CONSULTAS
# ==========================================
@app.route("/api/consultas", methods=["GET"])
def listar_consultas():
    query = """
        SELECT c.id, c.data, c.status,
               p.nome AS paciente_nome,
               pr.nome AS profissional_nome
        FROM consultas c
        LEFT JOIN pacientes p ON c.paciente_id = p.id
        LEFT JOIN profissionais pr ON c.profissional_id = pr.id
        ORDER BY c.data
    """
    with engine.connect() as conn:
        result = conn.execute(text(query)).mappings().all()
        return jsonify([dict(r) for r in result])


@app.route("/api/consultas", methods=["POST"])
def criar_consulta():
    data = request.json
    with engine.begin() as conn:
        conn.execute(
            text("""INSERT INTO consultas (paciente_id, profissional_id, data, status)
                    VALUES (:paciente_id, :profissional_id, :data, :status)"""),
            {
                "paciente_id": data["paciente_id"],
                "profissional_id": data["profissional_id"],
                "data": data["data"],
                "status": data.get("status", "agendada")
            }
        )
    return jsonify({"message": "Consulta criada com sucesso"}), 201


@app.route("/api/consultas/<int:id>", methods=["DELETE"])
def deletar_consulta(id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM consultas WHERE id = :id"), {"id": id})
    return jsonify({"message": "Consulta excluída com sucesso"})


# ==========================================
# ENTRADA
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

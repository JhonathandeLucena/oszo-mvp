import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text

# ================================
# Inicialização do Flask
# ================================
app = Flask(__name__)
CORS(app)

# ================================
# Configurações
# ================================
DATABASE_URL = os.getenv("DATABASE_URL")  # variável do Render
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN", "oszo-12345")

# Conexão com o banco de dados
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# ================================
# ROTAS DE SISTEMA
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
# ENDPOINTS PACIENTES
# ================================
@app.route("/api/pacientes", methods=["POST"])
def create_paciente():
    data = request.json
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO pacientes (nome, email) VALUES (:nome, :email)"),
                {"nome": data["nome"], "email": data.get("email")}
            )
        return jsonify({"message": "Paciente criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pacientes", methods=["GET"])
def list_pacientes():
    try:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT id, nome, email, criado_em FROM pacientes"))
            pacientes = [dict(row._mapping) for row in result]
        return jsonify(pacientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# ENDPOINTS PROFISSIONAIS
# ================================
@app.route("/api/profissionais", methods=["POST"])
def create_profissional():
    data = request.json
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO profissionais (nome, especialidade) VALUES (:nome, :especialidade)"),
                {"nome": data["nome"], "especialidade": data.get("especialidade")}
            )
        return jsonify({"message": "Profissional criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profissionais", methods=["GET"])
def list_profissionais():
    try:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT id, nome, especialidade, criado_em FROM profissionais"))
            profissionais = [dict(row._mapping) for row in result]
        return jsonify(profissionais)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# ENDPOINTS CONSULTAS
# ================================
@app.route("/api/consultas", methods=["POST"])
def create_consulta():
    data = request.json
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO consultas (paciente_id, profissional_id, data, status)
                    VALUES (:paciente_id, :profissional_id, :data, :status)
                """),
                {
                    "paciente_id": data["paciente_id"],
                    "profissional_id": data["profissional_id"],
                    "data": data["data"],
                    "status": data.get("status", "agendado")
                }
            )
        return jsonify({"message": "Consulta criada com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/consultas", methods=["GET"])
def list_consultas():
    try:
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT c.id, p.nome AS paciente, pr.nome AS profissional, 
                       c.data, c.status, c.criado_em
                FROM consultas c
                JOIN pacientes p ON c.paciente_id = p.id
                JOIN profissionais pr ON c.profissional_id = pr.id
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

# ================================
# ROTAS DE PACIENTES - UPDATE e DELETE
# ================================

@app.route("/api/pacientes/<int:paciente_id>", methods=["PUT"])
def atualizar_paciente(paciente_id):
    """Atualiza um paciente pelo ID"""
    data = request.json
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE pacientes
                    SET nome = :nome,
                        email = :email
                    WHERE id = :id
                """),
                {
                    "nome": data.get("nome"),
                    "email": data.get("email"),
                    "id": paciente_id
                }
            )
        return jsonify({"message": "Paciente atualizado com sucesso!", "status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pacientes/<int:paciente_id>", methods=["DELETE"])
def deletar_paciente(paciente_id):
    """Remove um paciente pelo ID"""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM pacientes WHERE id = :id"),
                {"id": paciente_id}
            )
        return jsonify({"message": "Paciente excluído com sucesso!", "status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# ROTAS DE PROFISSIONAIS - UPDATE e DELETE
# ================================

@app.route("/api/profissionais/<int:profissional_id>", methods=["PUT"])
def atualizar_profissional(profissional_id):
    """Atualiza um profissional pelo ID"""
    data = request.json
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE profissionais
                    SET nome = :nome,
                        especialidade = :especialidade
                    WHERE id = :id
                """),
                {
                    "nome": data.get("nome"),
                    "especialidade": data.get("especialidade"),
                    "id": profissional_id
                }
            )
        return jsonify({"message": "Profissional atualizado com sucesso!", "status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profissionais/<int:profissional_id>", methods=["DELETE"])
def deletar_profissional(profissional_id):
    """Remove um profissional pelo ID"""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM profissionais WHERE id = :id"),
                {"id": profissional_id}
            )
        return jsonify({"message": "Profissional excluído com sucesso!", "status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

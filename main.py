import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text
from werkzeug.exceptions import HTTPException
from functools import wraps

# ==========================================
# CONFIGURAÇÕES
# ==========================================
app = Flask(__name__)

# CORS apenas para Lovable e localhost
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://oszo-care-connect.lovable.app"
]}})

DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN", "oszo-12345")
API_TOKEN = os.getenv("API_TOKEN", "oszo-12345")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ==========================================
# AUTENTICAÇÃO (Bearer Token)
# ==========================================
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Endpoints públicos
        if request.endpoint in ["health", "init_db", "docs", "index"]:
            return f(*args, **kwargs)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": {"code": 401, "message": "Token ausente"}}), 401

        token = auth_header.split(" ")[1]
        if token != API_TOKEN:
            return jsonify({"error": {"code": 403, "message": "Token inválido"}}), 403

        return f(*args, **kwargs)
    return decorated

# ==========================================
# HANDLERS GLOBAIS DE ERRO
# ==========================================
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({"error": {"code": e.code, "message": e.description}}), e.code

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": {"code": 500, "message": str(e)}}), 500

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
        return jsonify({"error": {"code": 403, "message": "Token inválido"}}), 403

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
                    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
                    profissional_id INTEGER REFERENCES profissionais(id) ON DELETE CASCADE,
                    data TIMESTAMP,
                    status TEXT,
                    criado_em TIMESTAMP DEFAULT NOW()
                )
            """))
        return jsonify({"message": "Tabelas criadas com sucesso!", "status": "ok"})
    except Exception as e:
        return jsonify({"error": {"code": 500, "message": str(e)}}), 500

# ==========================================
# PACIENTES
# ==========================================
@app.route("/api/pacientes", methods=["GET"])
@require_auth
def listar_pacientes():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM pacientes")).mappings().all()
        return jsonify({"data": [dict(r) for r in result]})

@app.route("/api/pacientes", methods=["POST"])
@require_auth
def criar_paciente():
    data = request.json
    if not data.get("nome"):
        return jsonify({"error": {"code": 400, "message": "Nome é obrigatório"}}), 400
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO pacientes (nome, email) VALUES (:nome, :email)"),
            {"nome": data["nome"], "email": data.get("email")}
        )
    return jsonify({"message": "Paciente criado com sucesso"}), 201

@app.route("/api/pacientes/<int:id>", methods=["DELETE"])
@require_auth
def deletar_paciente(id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM pacientes WHERE id = :id"), {"id": id})
    return jsonify({"message": "Paciente excluído com sucesso"})

# ==========================================
# PROFISSIONAIS
# ==========================================
@app.route("/api/profissionais", methods=["GET"])
@require_auth
def listar_profissionais():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM profissionais")).mappings().all()
        return jsonify({"data": [dict(r) for r in result]})

@app.route("/api/profissionais", methods=["POST"])
@require_auth
def criar_profissional():
    data = request.json
    if not data.get("nome") or not data.get("especialidade"):
        return jsonify({"error": {"code": 400, "message": "Nome e especialidade são obrigatórios"}}), 400
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO profissionais (nome, especialidade) VALUES (:nome, :especialidade)"),
            {"nome": data["nome"], "especialidade": data["especialidade"]}
        )
    return jsonify({"message": "Profissional criado com sucesso"}), 201

@app.route("/api/profissionais/<int:id>", methods=["DELETE"])
@require_auth
def deletar_profissional(id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM profissionais WHERE id = :id"), {"id": id})
    return jsonify({"message": "Profissional excluído com sucesso"})

# ==========================================
# CONSULTAS
# ==========================================
@app.route("/api/consultas", methods=["GET"])
@require_auth
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
        return jsonify({"data": [dict(r) for r in result]})

@app.route("/api/consultas", methods=["POST"])
@require_auth
def create_consulta():
    data = request.get_json()
    paciente_id = data.get("paciente_id")
    profissional_id = data.get("profissional_id")
    consulta_data = data.get("data")
    status = data.get("status")

    if not paciente_id or not profissional_id or not consulta_data or not status:
        return jsonify({"error": {"code": 400, "message": "Campos obrigatórios: paciente_id, profissional_id, data, status"}}), 400

    from datetime import datetime
    try:
        dt = datetime.fromisoformat(consulta_data)
    except ValueError:
        return jsonify({"error": {"code": 400, "message": "Formato de data inválido. Use YYYY-MM-DDTHH:MM:SS"}}), 400

    with engine.begin() as conn:
        # Verifica paciente
        paciente = conn.execute(text("SELECT id FROM pacientes WHERE id = :id"), {"id": paciente_id}).fetchone()
        if not paciente:
            return jsonify({"error": {"code": 404, "message": f"Paciente id={paciente_id} não encontrado"}}), 404

        # Verifica profissional
        profissional = conn.execute(text("SELECT id FROM profissionais WHERE id = :id"), {"id": profissional_id}).fetchone()
        if not profissional:
            return jsonify({"error": {"code": 404, "message": f"Profissional id={profissional_id} não encontrado"}}), 404

        conn.execute(text("""
            INSERT INTO consultas (paciente_id, profissional_id, data, status)
            VALUES (:paciente_id, :profissional_id, :data, :status)
        """), {
            "paciente_id": paciente_id,
            "profissional_id": profissional_id,
            "data": dt,
            "status": status,
        })

    return jsonify({"message": "Consulta criada com sucesso!", "status": "ok"}), 201

@app.route("/api/consultas/<int:id>", methods=["DELETE"])
@require_auth
def deletar_consulta(id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM consultas WHERE id = :id"), {"id": id})
    return jsonify({"message": "Consulta excluída com sucesso"})

# ==========================================
# DOCS
# ==========================================
@app.route("/api/docs", methods=["GET"])
def docs():
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "OSZO Digital Health API", "version": "1.0.0"},
        "paths": {
            "/api/pacientes": {"get": {"summary": "Listar pacientes"}, "post": {"summary": "Criar paciente"}},
            "/api/profissionais": {"get": {"summary": "Listar profissionais"}, "post": {"summary": "Criar profissional"}},
            "/api/consultas": {"get": {"summary": "Listar consultas"}, "post": {"summary": "Criar consulta"}},
        }
    }
    return jsonify(spec)

# ==========================================
# ENTRADA
# ==========================================
@app.route("/")
def index():
    return jsonify({
        "message": "Bem-vindo à API OSZO 🚀",
        "endpoints": [
            "/health",
            "/api/admin/db/init?token=oszo-12345",
            "/api/pacientes",
            "/api/profissionais",
            "/api/consultas",
            "/api/docs"
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

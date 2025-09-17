import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from functools import wraps
from datetime import datetime

# =========================================
# Configurações iniciais
# =========================================
app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/oszo_db")
API_TOKEN = os.getenv("API_TOKEN", "oszo-12345")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# CORS
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://oszo-care-connect.lovable.app"
]}})

# =========================================
# Modelos
# =========================================
class Paciente(db.Model):
    __tablename__ = "pacientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Profissional(db.Model):
    __tablename__ = "profissionais"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    especialidade = db.Column(db.String(120), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Consulta(db.Model):
    __tablename__ = "consultas"
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey("profissionais.id", ondelete="CASCADE"), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    paciente = db.relationship("Paciente", backref=db.backref("consultas", cascade="all, delete-orphan"))
    profissional = db.relationship("Profissional", backref=db.backref("consultas", cascade="all, delete-orphan"))

# =========================================
# Autenticação via Bearer Token
# =========================================
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.endpoint in ["health", "init_db", "docs"]:
            return f(*args, **kwargs)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": {"code": 401, "message": "Token ausente ou formato inválido"}}), 401

        token = auth_header.split(" ")[1]
        if token != API_TOKEN:
            return jsonify({"error": {"code": 403, "message": "Token inválido"}}), 403

        return f(*args, **kwargs)
    return decorated

# =========================================
# Handlers de erro
# =========================================
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({"error": {"code": e.code, "message": e.description}}), e.code

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": {"code": 500, "message": "Erro interno do servidor"}}), 500

# =========================================
# Endpoints básicos
# =========================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "OSZO backend ativo"}), 200

@app.route("/api/admin/db/init", methods=["GET"])
@require_auth   # ⚠️ mantive protegido
def init_db():
    token = request.args.get("token")
    if token != API_TOKEN:
        return jsonify({"error": {"code": 403, "message": "Token inválido de init"}}), 403
    db.drop_all()
    db.create_all()
    return jsonify({"status": "ok", "message": "Banco inicializado com sucesso"}), 200

# =========================================
# CRUD Pacientes (SEM require_auth)
# =========================================
@app.route("/api/pacientes", methods=["GET"])
def listar_pacientes():
    pacientes = Paciente.query.all()
    data = [{"id": p.id, "nome": p.nome, "email": p.email, "criado_em": p.criado_em.isoformat()} for p in pacientes]
    return jsonify({"data": data}), 200

@app.route("/api/pacientes/<int:id>", methods=["GET"])
def get_paciente(id):
    p = Paciente.query.get(id)
    if not p:
        return jsonify({"error": {"code": 404, "message": f"Paciente id={id} não encontrado"}}), 404
    return jsonify({"data": {"id": p.id, "nome": p.nome, "email": p.email, "criado_em": p.criado_em.isoformat()}}), 200

@app.route("/api/pacientes", methods=["POST"])
def criar_paciente():
    body = request.get_json() or {}
    nome = body.get("nome")
    email = body.get("email")
    if not nome:
        return jsonify({"error": {"code": 400, "message": "Campo 'nome' é obrigatório"}}), 400
    try:
        novo = Paciente(nome=nome, email=email)
        db.session.add(novo)
        db.session.commit()
    except Exception as e:
        if "unique constraint" in str(e).lower():
            return jsonify({"error": {"code": 400, "message": "Email já existe"}}), 400
        raise
    return jsonify({"status": "ok", "message": "Paciente criado", "data": {"id": novo.id}}), 201

@app.route("/api/pacientes/<int:id>", methods=["PUT"])
def atualizar_paciente(id):
    p = Paciente.query.get(id)
    if not p:
        return jsonify({"error": {"code": 404, "message": f"Paciente id={id} não encontrado"}}), 404
    body = request.get_json() or {}
    if body.get("nome"):
        p.nome = body["nome"]
    if body.get("email"):
        existing = Paciente.query.filter(Paciente.email == body["email"], Paciente.id != id).first()
        if existing:
            return jsonify({"error": {"code": 400, "message": "Email já existe para outro paciente"}}), 400
        p.email = body["email"]
    db.session.commit()
    return jsonify({"status": "ok", "message": "Paciente atualizado", "data": {"id": p.id}}), 200

@app.route("/api/pacientes/<int:id>", methods=["DELETE"])
def deletar_paciente(id):
    p = Paciente.query.get(id)
    if not p:
        return jsonify({"error": {"code": 404, "message": f"Paciente id={id} não encontrado"}}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"status": "ok", "message": "Paciente excluído"}), 200

# =========================================
# CRUD Profissionais (SEM require_auth)
# =========================================
@app.route("/api/profissionais", methods=["GET"])
def listar_profissionais():
    pro = Profissional.query.all()
    data = [{"id": pr.id, "nome": pr.nome, "especialidade": pr.especialidade, "criado_em": pr.criado_em.isoformat()} for pr in pro]
    return jsonify({"data": data}), 200

@app.route("/api/profissionais/<int:id>", methods=["GET"])
def get_profissional(id):
    pr = Profissional.query.get(id)
    if not pr:
        return jsonify({"error": {"code": 404, "message": f"Profissional id={id} não encontrado"}}), 404
    return jsonify({"data": {"id": pr.id, "nome": pr.nome, "especialidade": pr.especialidade, "criado_em": pr.criado_em.isoformat()}}), 200

@app.route("/api/profissionais", methods=["POST"])
def criar_profissional():
    body = request.get_json() or {}
    nome = body.get("nome")
    especialidade = body.get("especialidade")
    if not nome:
        return jsonify({"error": {"code": 400, "message": "Campo 'nome' é obrigatório"}}), 400
    novo = Profissional(nome=nome, especialidade=especialidade)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"status": "ok", "message": "Profissional criado", "data": {"id": novo.id}}), 201

@app.route("/api/profissionais/<int:id>", methods=["PUT"])
def atualizar_profissional(id):
    pr = Profissional.query.get(id)
    if not pr:
        return jsonify({"error": {"code": 404, "message": f"Profissional id={id} não encontrado"}}), 404
    body = request.get_json() or {}
    if body.get("nome"):
        pr.nome = body["nome"]
    if body.get("especialidade") is not None:
        pr.especialidade = body["especialidade"]
    db.session.commit()
    return jsonify({"status": "ok", "message": "Profissional atualizado", "data": {"id": pr.id}}), 200

@app.route("/api/profissionais/<int:id>", methods=["DELETE"])
def deletar_profissional(id):
    pr = Profissional.query.get(id)
    if not pr:
        return jsonify({"error": {"code": 404, "message": f"Profissional id={id} não encontrado"}}), 404
    db.session.delete(pr)
    db.session.commit()
    return jsonify({"status": "ok", "message": "Profissional excluído"}), 200

# =========================================
# CRUD Consultas (SEM require_auth)
# =========================================
@app.route("/api/consultas", methods=["GET"])
def listar_consultas():
    cs = Consulta.query.order_by(Consulta.data).all()
    data = []
    for c in cs:
        data.append({
            "id": c.id,
            "paciente": {"id": c.paciente.id, "nome": c.paciente.nome},
            "profissional": {"id": c.profissional.id, "nome": c.profissional.nome},
            "data": c.data.isoformat(),
            "status": c.status,
            "criado_em": c.criado_em.isoformat()
        })
    return jsonify({"data": data}), 200

@app.route("/api/consultas/<int:id>", methods=["GET"])
def get_consulta(id):
    c = Consulta.query.get(id)
    if not c:
        return jsonify({"error": {"code": 404, "message": f"Consulta id={id} não encontrada"}}), 404
    return jsonify({"data": {
        "id": c.id,
        "paciente": {"id": c.paciente.id, "nome": c.paciente.nome},
        "profissional": {"id": c.profissional.id, "nome": c.profissional.nome},
        "data": c.data.isoformat(),
        "status": c.status,
        "criado_em": c.criado_em.isoformat()
    }}), 200

@app.route("/api/consultas", methods=["POST"])
def criar_consulta():
    body = request.get_json() or {}
    paciente_id = body.get("paciente_id")
    profissional_id = body.get("profissional_id")
    data_str = body.get("data")
    status = body.get("status")

    if not paciente_id or not profissional_id or not data_str or not status:
        return jsonify({"error": {"code": 400, "message": "Campos obrigatórios: paciente_id, profissional_id, data, status"}}), 400

    paciente = Paciente.query.get(paciente_id)
    if not paciente:
        return jsonify({"error": {"code": 404, "message": f"Paciente id={paciente_id} não encontrado"}}), 404

    profissional = Profissional.query.get(profissional_id)
    if not profissional:
        return jsonify({"error": {"code": 404, "message": f"Profissional id={profissional_id} não encontrado"}}), 404

    try:
        data_obj = datetime.fromisoformat(data_str)
    except ValueError:
        return jsonify({"error": {"code": 400, "message": "Formato de data inválido. Use ISO 8601"}}), 400

    novo = Consulta(paciente_id=paciente_id, profissional_id=profissional_id, data=data_obj, status=status)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"status": "ok", "message": "Consulta criada", "data": {"id": novo.id}}), 201

@app.route("/api/consultas/<int:id>", methods=["PUT"])
def atualizar_consulta(id):
    c = Consulta.query.get(id)
    if not c:
        return jsonify({"error": {"code": 404, "message": f"Consulta id={id} não encontrada"}}), 404
    body = request.get_json() or {}
    if body.get("paciente_id"):
        paciente_id = body["paciente_id"]
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({"error": {"code": 404, "message": f"Paciente id={paciente_id} não encontrado"}}), 404
        c.paciente_id = paciente_id
    if body.get("profissional_id"):
        profissional_id = body["profissional_id"]
        profissional = Profissional.query.get(profissional_id)
        if not profissional:
            return jsonify({"error": {"code": 404, "message": f"Profissional id={profissional_id} não encontrado"}}), 404
        c.profissional_id = profissional_id
    if body.get("data"):
        try:
            c.data = datetime.fromisoformat(body["data"])
        except ValueError:
            return jsonify({"error": {"code": 400, "message": "Formato de data inválido"}}), 400
    if body.get("status"):
        c.status = body["status"]
    db.session.commit()
    return jsonify({"status": "ok", "message": "Consulta atualizada", "data": {"id": c.id}}), 200

@app.route("/api/consultas/<int:id>", methods=["DELETE"])
def deletar_consulta(id):
    c = Consulta.query.get(id)
    if not c:
        return jsonify({"error": {"code": 404, "message": f"Consulta id={id} não encontrada"}}), 404
    db.session.delete(c)
    db.session.commit()
    return jsonify({"status": "ok", "message": "Consulta excluída"}), 200

# =========================================
# Docs
# =========================================
@app.route("/api/docs", methods=["GET"])
def docs():
    return jsonify({"info": "Documentação básica da OSZO Digital Health API"}), 200

# =========================================
# Execução
# =========================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

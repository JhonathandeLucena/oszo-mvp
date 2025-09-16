import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN", "oszo-12345")

engine = create_engine(DATABASE_URL)

@app.route("/api/admin/db/init")
def init_db():
    token = request.args.get("token")
    if token != ADMIN_INIT_TOKEN:
        return jsonify({"error": "Token inválido"}), 403

    try:
        with engine.connect() as conn:
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

        return jsonify({"message": "Tabelas criadas com sucesso!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
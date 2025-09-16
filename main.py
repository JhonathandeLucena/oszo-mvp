from flask import Flask, jsonify

# Criação do app Flask
app = Flask(__name__)

# Rota de teste (health check)
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "OSZO backend rodando no Render 🚀"
    })

# Executa localmente (Render usará o Gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
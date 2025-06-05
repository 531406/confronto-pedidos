from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "API de Confronto de Pedidos e Cargas"

@app.route('/upload', methods=['POST'])
def upload_files():
    resumo = request.files.get('resumo')
    pedidos = request.files.getlist('pedidos')
    vinculos = request.form.get('vinculos')

    if not resumo or not pedidos or not vinculos:
        return jsonify({"error": "Dados incompletos"}), 400

    resumo_path = os.path.join(UPLOAD_FOLDER, secure_filename(resumo.filename))
    resumo.save(resumo_path)

    pedidos_paths = []
    for pedido in pedidos:
        path = os.path.join(UPLOAD_FOLDER, secure_filename(pedido.filename))
        pedido.save(path)
        pedidos_paths.append(path)

    # Simulação do confronto
    return jsonify({
        "status": "Confronto simulado com sucesso",
        "resumo_recebido": resumo.filename,
        "quantidade_pedidos": len(pedidos),
        "vinculos": vinculos
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS  # Importando o CORS
import fitz  # PyMuPDF para ler os arquivos PDF

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer domínio

# Função para extrair texto de um PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Rota principal para testar a API
@app.route('/')
def home():
    return "API de Confronto de Pedidos e Cargas"

# Rota para processar o upload dos arquivos
@app.route('/upload', methods=['POST'])
def upload_files():
    resumo = request.files.get('resumo')  # Arquivo de resumo de carga
    pedidos = request.files.getlist('pedidos')  # Vários arquivos de pedidos
    vinculos = request.form.get('vinculos')  # Dados de vinculação de pedidos e rotas

    # Se não houver arquivos ou vinculações, retorna um erro
    if not resumo or not pedidos or not vinculos:
        return jsonify({"error": "Dados incompletos"}), 400

    # Extraindo o texto do Resumo de Carga (PDF)
    resumo_text = extract_text_from_pdf(resumo)

    pedidos_texts = []
    for pedido in pedidos:
        pedido_text = extract_text_from_pdf(pedido)
        pedidos_texts.append(pedido_text)

    # Aqui você pode implementar a lógica de comparação entre o resumo e os pedidos.
    # No momento, vamos apenas simular o confronto e retornar o texto extraído.

    return jsonify({
        "status": "Confronto realizado com sucesso",
        "resumo_recebido": resumo.filename,
        "resumo_texto": resumo_text[:500],  # Mostra os primeiros 500 caracteres do texto extraído
        "quantidade_pedidos": len(pedidos),
        "pedidos_texto": [pedido[:500] for pedido in pedidos_texts],  # Mostra os primeiros 500 caracteres de cada pedido
        "vinculos": vinculos
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Definindo o servidor para rodar na porta 5000
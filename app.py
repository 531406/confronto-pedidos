import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "API de Confronto de Pedidos e Cargas"

# Função para ler o conteúdo do arquivo PDF
def ler_pdf(caminho_arquivo):
    # Abrir o PDF com PyMuPDF
    doc = fitz.open(caminho_arquivo)
    texto = ""
    
    # Iterar sobre todas as páginas e extrair o texto
    for pagina in doc:
        texto += pagina.get_text()
    
    return texto

# Endpoint para upload de arquivos
@app.route('/upload', methods=['POST'])
def upload_files():
    # Verifica se os arquivos foram enviados
    if 'resumo' not in request.files or 'pedidos' not in request.files:
        return jsonify({'error': 'Arquivo de resumo ou pedidos não enviado.'}), 400
    
    resumo = request.files['resumo']
    pedidos = request.files.getlist('pedidos')

    # Salvar o arquivo resumo temporariamente para ler o conteúdo
    resumo.save("resumo_temp.pdf")
    
    # Lendo o conteúdo do arquivo resumo
    texto_resumo = ler_pdf("resumo_temp.pdf")
    
    # Aqui você pode processar o texto extraído conforme necessário
    # Exibindo uma parte do conteúdo para teste
    preview_texto_resumo = texto_resumo[:500]  # Exibindo os primeiros 500 caracteres
    
    # Retornar uma resposta com o conteúdo lido do PDF (apenas como exemplo)
    return jsonify({
        'status': 'success',
        'preview_resumo': preview_texto_resumo,
        'total_pedidos': len(pedidos)
    })

# Garantir que a aplicação escute em qualquer IP e na porta definida pelo Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render define a variável de ambiente PORT
    app.run(host="0.0.0.0", port=port)

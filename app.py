import os
from flask import Flask, request, jsonify
import secrets
import string

app = Flask(__name__)

@app.route('/')
def home():
    return "API Gerador de Senhas Bancárias está no ar!"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/gerar-senha')
def gerar_senha():
    # Parâmetros opcionais
    try:
        comprimento = int(request.args.get('comprimento', 12))
        maiusculas = request.args.get('maiusculas', 'true').lower() == 'true'
        minusculas = request.args.get('minusculas', 'true').lower() == 'true'
        numeros = request.args.get('numeros', 'true').lower() == 'true'
        especiais = request.args.get('especiais', 'true').lower() == 'true'
    except ValueError:
        return jsonify({"error": "Parâmetro 'comprimento' deve ser um inteiro"}), 400

    # Validação
    if not (8 <= comprimento <= 128):
        return jsonify({"error": "Comprimento deve estar entre 8 e 128"}), 400

    if not (maiusculas or minusculas or numeros or especiais):
        return jsonify({"error": "Pelo menos um tipo de caractere deve ser selecionado"}), 400

    # Construir conjunto de caracteres
    chars = ''
    if maiusculas:
        chars += string.ascii_uppercase
    if minusculas:
        chars += string.ascii_lowercase
    if numeros:
        chars += string.digits
    if especiais:
        chars += string.punctuation

    # Garantir que a senha tenha pelo menos um de cada tipo selecionado
    senha = []
    if maiusculas:
        senha.append(secrets.choice(string.ascii_uppercase))
    if minusculas:
        senha.append(secrets.choice(string.ascii_lowercase))
    if numeros:
        senha.append(secrets.choice(string.digits))
    if especiais:
        senha.append(secrets.choice(string.punctuation))

    # Preencher o resto
    while len(senha) < comprimento:
        senha.append(secrets.choice(chars))

    # Embaralhar
    secrets.SystemRandom().shuffle(senha)
    senha_str = ''.join(senha)

    return jsonify({"senha": senha_str})

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host=host, port=port, debug=debug)

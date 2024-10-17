from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json

app = Flask(__name__)

# Função para carregar dados de usuários do arquivo dados.js (ou criar o arquivo se não existir)
def carregar_dados_usuarios():
    if not os.path.exists('dados.js'):
        with open('dados.js', 'w') as f:
            json.dump([], f)
    with open('dados.js', 'r') as f:
        return json.load(f)

# Função para salvar novos dados de usuários
def salvar_dados_usuarios(usuarios):
    with open('dados.js', 'w') as f:
        json.dump(usuarios, f)

# Rota para a página inicial (registro e login juntos)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para registrar novo usuário
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    nome_usuario = request.form.get('nome_usuario')
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuarios = carregar_dados_usuarios()

    # Verificar se o nome de usuário já existe
    for usuario in usuarios:
        if usuario['nome_usuario'] == nome_usuario:
            return jsonify({'status': 'error', 'message': 'Nome de usuário já existe.'})

    # Criar novo usuário e adicionar ao arquivo
    novo_usuario = {
        'nome_usuario': nome_usuario,
        'email': email,
        'senha': senha
    }
    usuarios.append(novo_usuario)
    salvar_dados_usuarios(usuarios)

    # Criar uma pasta para o novo usuário onde suas postagens serão armazenadas
    pasta_usuario = os.path.join('usuarios', nome_usuario)
    os.makedirs(pasta_usuario)
    os.makedirs(os.path.join(pasta_usuario, 'img'))
    os.makedirs(os.path.join(pasta_usuario, 'videos'))
    os.makedirs(os.path.join(pasta_usuario, 'textos'))

    return jsonify({'status': 'success', 'message': 'Usuário registrado com sucesso!'})

# Rota para verificar login
@app.route('/login', methods=['POST'])
def verificar_login():
    nome_usuario = request.form.get('nome_usuario')
    senha = request.form.get('senha')

    usuarios = carregar_dados_usuarios()

    # Verifica se o usuário existe e a senha está correta
    for usuario in usuarios:
        if usuario['nome_usuario'] == nome_usuario and usuario['senha'] == senha:
            # Redireciona para o perfil do usuário
            return redirect(url_for('perfil_usuario', nome_usuario=nome_usuario))

    return jsonify({'status': 'error', 'message': 'Nome de usuário ou senha incorretos'})

# Rota para o perfil do usuário
@app.route('/usuario/<nome_usuario>')
def perfil_usuario(nome_usuario):
    user_folder = os.path.join('usuarios', nome_usuario)
    
    # Carregar imagens, vídeos e textos
    imagens = os.listdir(os.path.join(user_folder, 'img'))
    videos = os.listdir(os.path.join(user_folder, 'videos'))
    textos = os.listdir(os.path.join(user_folder, 'textos'))

    return render_template('perfil.html', nome_usuario=nome_usuario, imagens=imagens, videos=videos, textos=textos)

if __name__ == '__main__':
    app.run(debug=True)

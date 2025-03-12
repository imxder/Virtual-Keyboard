
from flask import Flask, render_template, redirect, request, flash, jsonify
import mysql.connector
from datetime import datetime
import bcrypt
import warnings

from servidor import Servidor
from sessoes import Sessoes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PASSPASS'

servidor = Servidor()
sessoes = Sessoes()

warnings.filterwarnings("ignore", category=UserWarning)

def int_to_list(number):
    if number is None or not str(number).isdigit():
        return []
    return [int(digit) for digit in str(number)]

@app.route('/')
def home():
    
    sequencia_numeros = Sessoes().BuscarSessaoValida()
    sequencia_numeros = int_to_list(sequencia_numeros)
    print(sequencia_numeros)
    return render_template('login.html', sequencia=sequencia_numeros)


@app.route('/criarSessoes', methods=['GET'])
def CriarSessoes():
    try:
        Sessoes().GerarSessoes()
        return jsonify({"Mensagem": "Conta autenticada com sucesso"}), 200
    except Exception:
        return jsonify({"Erro": "Ocorreu um erro desconhecido"}), 500

@app.route('/buscarSessao', methods=['GET'])
def BuscarSessao():
    try:
        endereco_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        print(f"Endereço IP: {endereco_ip}")
        
        HashRetorno, OrdemRetorno = Sessoes().BuscarSessaoValida()
        return jsonify({"Hash": HashRetorno, "Ordem": OrdemRetorno}), 200
    except Exception:
        return jsonify({"Erro": "Ocorreu um erro desconhecido"}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = request.form.get('user')
    senha = request.form.get('senha')

    try:
        mydb = servidor.conecta()
        if mydb.is_connected():
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM usuario WHERE user = %s;", (user,))
            usuarioBD = cursor.fetchall()

            if not usuarioBD:
                print("Conta não encontrada")
                return redirect('/')

            numeros = [char for char in senha if char.isdigit()]
            if len(numeros) < 8:
                print("Senha inválida")
                return redirect('/')

            combinacoes = [
                f"{numeros[i]}{numeros[j]}{numeros[k]}{numeros[l]}"
                for i in range(2) for j in range(2, 4)
                for k in range(4, 6) for l in range(6, 8)
            ]

            hash_senha = usuarioBD[0][2].encode('utf-8')

            for senha_verif in combinacoes:
                senha_bytes = senha_verif.encode('utf-8')
                if bcrypt.checkpw(senha_bytes, hash_senha):
                    cursor.close()
                    mydb.close()
                    return redirect('/usuarios')

            print("Senha incorreta")
            cursor.close()
            mydb.close()
            return redirect('/')

    except Exception as ex:
        print(f"Erro ao executar a consulta: {ex}")
        return redirect('/')

@app.route('/usuarios')
def usuarios():
    return render_template("usuarios.html")

@app.route('/path')
def path():
    return render_template("cadastrar.html")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    try:
        user = request.form.get('user')
        senha = request.form.get('senha')

        if len(senha) != 4 or not senha.isdigit():
            print("A senha deve ter 4 caracteres numéricos.")
            return redirect('/path')

        mydb = servidor.conecta()
        cursor = mydb.cursor()
        cursor.execute("SELECT user FROM usuario WHERE user = %s", (user,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            print("Usuário já cadastrado!")
            return redirect('/path')

        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt(6)).decode('utf-8')
        data_hora_atual = datetime.now()

        cursor.execute("INSERT INTO usuario VALUES (default, %s, %s, %s)", (user, hashed_senha, data_hora_atual))
        mydb.commit()
        print("Usuário cadastrado com sucesso")

        cursor.close()
        mydb.close()

    except mysql.connector.errors.IntegrityError as e:
        if 'Duplicate entry' in str(e):
            print("Usuário já cadastrado!")
        else:
            print("Erro ao cadastrar usuário")
        return redirect('/path')

    return redirect('/')

if __name__ == '__main__':
    app.run(host="localhost", port=3308, debug=True, use_reloader=False)

from flask import Flask, render_template, redirect, request, flash, jsonify
import mysql.connector
from datetime import datetime
import bcrypt
import warnings


from servidor import Servidor
from sessoes import Sessoes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PASSPASS'

# pool = mysql.connector.pooling.MySQLConnectionPool(
#     host="localhost",
#     user="root",
#     password="Semestre202301",
#     database="users",
#     pool_size=32,
# )
servidor = Servidor()
sessoes = Sessoes()


warnings.filterwarnings("ignore", category = UserWarning)

# @app.route('/')
# def home():
#     return render_template('login.html')

@app.route('/')
def home():
    sequencia_numeros = Sessoes().BuscarSessaoValida()
    sequencia_numeros = int_to_list(sequencia_numeros)
    print(sequencia_numeros)
    return render_template('login.html', sequencia=sequencia_numeros)

def int_to_list(number):
    return [int(digit) for digit in str(number)]
 






@app.route('/criarSessoes', methods = ['GET'])
def CriarSessoes():
   try:
      Sessoes().GerarSessoes()
      return jsonify({"Mensagem": "Conta autenticada com sucesso"}), int(200)
   except Exception as erro:
      return 'Ocorreu um erro desconhecido', 500
   

@app.route('/buscarSessao', methods = ['GET'])
def BuscarSessao():
   try:
      endereco_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
      print("Endereço ip: " +str(endereco_ip))
      HashRetorno, OrdemRetorno = Sessoes().BuscarSessaoValida()
      return jsonify({"Hash: ": HashRetorno, 'Ordem': OrdemRetorno}), int(200)
   except Exception as erro:
      return 'Ocorreu um erro desconhecido', 500


# @app.route('/login', methods=['POST']) ------------------Última versão estável
# def login():
#   cont = 0
#   user = request.form.get('user')
#   senha = request.form.get('senha')

#   try:
#     mydb = servidor.conecta()

#     if mydb.is_connected():
#       cursor = mydb.cursor()
#       cursor.execute('SELECT * FROM usuario;')
#       usuariosBD = cursor.fetchall()

#       for usuario in usuariosBD:
#         cont += 1
#         usuarioUser = str(usuario[1])
#         usuarioSenha = str(usuario[2])

#         # Validação da senha com bcrypt
#         if usuarioUser == user and usuarioSenha == senha:
#           return redirect('/usuarios')

#       if cont >= len(usuariosBD):
#         return redirect('/')

#       cursor.close()
#       mydb.close()

#   except Exception as e:
#     print(f"Erro ao executar a consulta: {e}")
#     return redirect('/')

#   return redirect('/')

@app.route('/login', methods=['GET','POST'])
def login():
#   cont = 0
  user = request.form.get('user')
  senha = request.form.get('senha')

  try:
    # Conexão com o banco de dados
    mydb = servidor.conecta()
    query = f"SELECT * FROM usuario WHERE user = '{user}';"

    if mydb.is_connected():
      cursor = mydb.cursor()
      cursor.execute(query)
      usuarioBD = cursor.fetchall()

      if len(usuarioBD) <=0:
        print("Conta não encontrada")
        return False, 'Conta não encontrada'
      numeros = list(filter(lambda char: char.isdigit(), senha))
      a = [numeros[0], numeros[1]]
      b = [numeros[2], numeros[3]]
      c = [numeros[4], numeros[5]]
      d = [numeros[6], numeros[7]]
      for i in a:
           for j in b:
               for k in c:
                   for l in d:
                      senha_verif = f"{i}{j}{k}{l}"
                    #   print(senha_verif)
                      hash_senha = usuarioBD[0][2]
                      senha_bytes = senha_verif.encode('utf-8')
                      hashed_password_bytes = hash_senha.encode('utf-8')
      
    #   print(hash_senha)
    #   print(senha)
                      if bcrypt.checkpw(senha_bytes, hashed_password_bytes):
                         return redirect('/usuarios')
                      
      print("Senha incorreta")
      return redirect('/')
         
    

      
    #   hash_senha = usuarioBD[0][0]
    #   a = [senha[0], senha[1]]
    #   b = [senha[2], senha[3]]
    #   c = [senha[4], senha[5]]
    #   d = [senha[6], senha[7]]
    #   e = [senha[8], senha[9]]
    #   for i in a:
    #       for j in b:
    #           for k in c:
    #               for l in d:
    #                   for m in e:
    #                       SenhaVerif = f"{i}{j}{k}{l}{m}"
    #                       if bcrypt.verify(SenhaVerif, hash_senha):
    #                           return redirect('/usuarios')
      
    cursor.close()
    mydb.close()

    
  except Exception as ex:
    print(f"Erro ao executar a consulta: {ex}")
    return redirect('/')

@app.route('/usuarios')
def usuarios():
    return render_template("usuarios.html")

@app.route('/path')
def path():
    return render_template("cadastrar.html")

# @app.route('/show_login_form')
# def show_login_form():
#     return redirect('/login')


@app.route('/cadastrarUsuario', methods = ['POST'])
def cadastrarUsuario():
    try:
        # mydb = servidor.conecta()
        user = request.form.get('user')
        mydb = servidor.conecta()
        cursor = mydb.cursor()
        cursor.execute("SELECT user FROM usuario WHERE user = %s", (user,))
        usuario_existente = cursor.fetchone()
        # cursor.close()
        # mydb.close()

        if usuario_existente:
            print("Usuário já cadastrado!")
            return redirect('/path')
        senha = request.form.get('senha')
        data_hora_atual = datetime.now()

        if len(senha) != 4:
            print("A senha deve ter entre 4 caracteres.")
            return redirect('/path')
        if not all(char.isdigit() for char in senha):
            print("A senha deve conter apenas números.")
            return redirect('/path')
        
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt(6))
        cursor = mydb.cursor(prepared = True)
        # cursor.execute(f"INSERT INTO usuario VALUES (default, '{user}', '{hashed_senha}', '{data_hora_atual}');")
        sql = f"INSERT INTO usuario VALUES (default, %s, %s, %s);"
        cursor.execute(sql, (user, hashed_senha, data_hora_atual))
        mydb.commit()
        print("Usuário cadastrado com sucesso")
    except mysql.connector.errors.IntegrityError as e:
        if 'Duplicate entry' in e.args[1]:
            print("Usuário já cadastrado!")
            return redirect('/path') 
        else:
            print("Erro ao cadastrar usuário")
        return redirect('/path') 

    if mydb.is_connected():
        mydb.close()

    return redirect('/')
    

if __name__ == '__main__':
    app.run(host="localhost", port="5000", debug=True, use_reloader = "False")
import bcrypt
import random
import datetime as datetime

from servidor import Servidor
servidor = Servidor()

class Sessoes():
    def gerar_sequencia(self):
        digitos_unicos = random.sample(range(10), 10)
        # print("Digitos unicos")
        # print(digitos_unicos)
        return ''.join(map(str, digitos_unicos))
    

    def GerarSessoes(self):
        dados = [self.gerar_sequencia() for _ in range(10)]
        for dado in dados:
            valor_aleatorio = str(random.randint(0, 9999))
            hash_obj = bcrypt.hashpw(valor_aleatorio.encode('utf-8'), bcrypt.gensalt(6))
            # hash_calculado = hash_obj.decode('utf-8').hexdigest()
            mydb = servidor.conecta()
            mydb = servidor.inserirSessoes(hash_obj, dado)

    def BuscarSessaoValida(self):
        # mydb = servidor.conecta()
        # mydb = servidor.LiberarSessoes()
        # linha = servidor.buscarDado('Sessoes', 'hash, ordem', f'disponivel = 1')
        # hashRetorno = linha[0][0]
        # OrdemRetorno = linha[0][1]
        # servidor.AtualizarRegistro('Sessoes', 'disponivel = 0, ultima_vez_usado = GETDATE()', f"hash = '{hashRetorno}'")
        # return hashRetorno, OrdemRetorno
        try:
            data_atual = datetime.datetime.now()
            mydb = servidor.conecta()
            cursor = mydb.cursor(prepared=True)

            query = "SELECT hash, ordem FROM sessoes WHERE disponivel = 1 ORDER BY ultima_vez_usado ASC LIMIT 1;"
            cursor.execute(query)

            linha = cursor.fetchone()

            if linha is not None:
                hash_retorno  = linha[0]
                ordem_retorno = linha[1]
                print("O erro é aqui mesmooooo")
                print(ordem_retorno)
                query = "UPDATE sessoes SET disponivel = 0, ultima_vez_usado = %s WHERE hash = %s"
                cursor.execute(query, (data_atual, hash_retorno))
                mydb.commit()
            else:
                print("Nenhuma sessão disponível")

            cursor.close()
            mydb.close()
            print(ordem_retorno)
            return ordem_retorno

        except Exception as e:
            print(f"Erro ao buscar sessão válida: {e}")



def executar():
    sessao = Sessoes()
    sessao.GerarSessoes()

# executar()


import bcrypt
import random
import datetime
from servidor import Servidor

servidor = Servidor()

class Sessoes:
    def gerar_sequencia(self):
        return ''.join(map(str, random.sample(range(10), 10)))

    def GerarSessoes(self):
       
        try:
            mydb = servidor.conecta()
            cursor = mydb.cursor()

            for _ in range(10):
                dado = self.gerar_sequencia()
                valor_aleatorio = str(random.randint(0, 9999))

                hash_obj = bcrypt.hashpw(valor_aleatorio.encode('utf-8'), bcrypt.gensalt(6))
                hash_str = hash_obj.decode('utf-8')

                servidor.inserirSessoes(hash_str, dado)  

            cursor.close()
            mydb.close()

        except Exception as e:
            print(f"Erro ao gerar sessões: {e}")

    def BuscarSessaoValida(self):
        
        try:
            mydb = servidor.conecta()
            cursor = mydb.cursor()

            
            query = "SELECT hash, ordem FROM sessoes WHERE disponivel = 1 ORDER BY ultima_vez_usado ASC LIMIT 1;"
            cursor.execute(query)
            linha = cursor.fetchone()

            if linha:
                hash_retorno, ordem_retorno = linha
                print(f"Encontrada sessão válida: {ordem_retorno}")

                
                data_atual = datetime.datetime.now()
                query = "UPDATE sessoes SET disponivel = 0, ultima_vez_usado = %s WHERE hash = %s"
                cursor.execute(query, (data_atual, hash_retorno))
                mydb.commit()

                cursor.close()
                mydb.close()
                return ordem_retorno
            else:
                print("Nenhuma sessão disponível")
                cursor.close()
                mydb.close()
                return None

        except Exception as e:
            print(f"Erro ao buscar sessão válida: {e}")
            return None

def executar():
    sessao = Sessoes()
    sessao.GerarSessoes()



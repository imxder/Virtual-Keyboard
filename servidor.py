import mysql.connector
import datetime

class Servidor:
    def __init__(self):
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            host="localhost",
            user="root",
            password="",
            database="users",
            pool_size=10,  
        )

    def conecta(self):   
        try:
            return self.pool.get_connection()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def buscarDados(self, tabela, coluna="*", condicao=None): 
        try:
            with self.conecta() as mydb:
                with mydb.cursor() as cursor:
                    query = f"SELECT {coluna} FROM {tabela}"
                    if condicao:
                        query += f" WHERE {condicao}"
                    cursor.execute(query)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")
            return []

    def buscarDado(self, tabela, coluna="*", condicao=None):
        try:
            with self.conecta() as mydb:
                with mydb.cursor() as cursor:
                    query = f"SELECT {coluna} FROM {tabela}"
                    if condicao:
                        query += f" WHERE {condicao}"
                    query += " LIMIT 1"
                    cursor.execute(query)
                    return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")
            return None

    def inserirSessoes(self, hashEntrada, ordemNumeros):
        """Insere uma nova sessão"""
        try:
            with self.conecta() as mydb:
                with mydb.cursor() as cursor:
                    query = """
                        INSERT INTO sessoes (hash, ordem, disponivel, ultima_vez_usado)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (hashEntrada, ordemNumeros, 1, datetime.datetime.now()))
                    mydb.commit()
                    print("Sessão inserida com sucesso!")
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")

    def AtualizarRegistro(self, tabela, colunas, condicao):
        try:
            with self.conecta() as mydb:
                with mydb.cursor() as cursor:
                    query = f"UPDATE {tabela} SET {colunas} WHERE {condicao}"
                    cursor.execute(query)
                    mydb.commit()
        except Exception as e:
            print(f"Erro ao executar atualização: {e}")

    def LiberarSessoes(self):
        try:
            registros = self.buscarDados(
                "sessoes", "id",
                "disponivel = 0 AND TIMESTAMPDIFF(MINUTE, ultima_vez_usado, NOW()) > 10"
            )
            for idRetornado in registros:
                self.AtualizarRegistro("sessoes", "disponivel = 1", f"id = {idRetornado[0]}")
        except Exception as e:
            print(f"Erro ao liberar sessões: {e}")

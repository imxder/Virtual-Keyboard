import datetime
import pyodbc

class SQLServer:
    def __init__(self):
        self.server = 'Mindinho'
        self.database = 'Advanced'
        self.user = 'vini1'
        self.senha = 'senhasenha'
        self.conexao = None
        self.cursor = None
        self.conexaoBanco()

    def conexaoBanco(self):
        try:
            dados = (
                "Driver={ODBC Driver 17 for SQL Server};"
                f"Server={self.server};"
                f"Database={self.database};"
                "Trusted_Connection=no;"
                f"UID={self.user};"
                f"PWD={self.senha};"
            )
            self.conexao = pyodbc.connect(dados)
            self.cursor = self.conexao.cursor()
        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def inserirDadosUsuario(self,agencia,conta,senha):
        self.conexaoBanco()
        if len(senha) < 4:
            return "Senha muito curta"
        query = f"insert into Usuarios(agencia,conta,senha,ultima_vez_logado) values ('{agencia}',{conta},'{senha}',GETDATE())"
        self.cursor.execute(query)
        self.cursor.commit()
        self.conexao.close()

    def buscarDados(self, tabela, coluna="*", condicao=None):
        try:
            self.conexaoBanco()
            query = f"SELECT {coluna} FROM {tabela}"
            if condicao:
                query += f" WHERE {condicao}"
            self.cursor.execute(query)
            linhas = self.cursor.fetchall()
            self.conexao.close()
            return linhas
        except pyodbc.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            
    def buscarDado(self, tabela, coluna="*", condicao=None):
        try:
            self.conexaoBanco()
            query = f"SELECT TOP 1 {coluna} FROM {tabela}"
            if condicao:
                query += f" WHERE {condicao}"
            self.cursor.execute(query)
            linhas = self.cursor.fetchall()
            self.conexao.close()
            return linhas
        except pyodbc.Error as e:
            print(f"Erro ao executar a consulta: {e}")

    def inserirSessoes(self,hashEntrada,ordemNumeros):
        self.conexaoBanco()
        query = f"insert into Sessoes(hash,ordem,disponivel,ultima_vez_usado) values ('{hashEntrada}',{ordemNumeros},1,GETDATE())"
        self.cursor.execute(query)
        self.cursor.commit()
        self.conexao.close()
        
    def AtualizarRegistro(self, tabela, colunas, condicao):
        try:
            self.conexaoBanco()
            query = f"UPDATE {tabela}  SET {colunas} WHERE {condicao}"
            self.cursor.execute(query)
            self.cursor.commit()
            self.conexao.close()
        except pyodbc.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            
    def LiberarSessoes(self):
        try:
            Ids = self.buscarDados("Sessoes", 'id', "disponivel = 0 and DATEADD(MINUTE, 10, ultima_vez_usado) < GETDATE()")
            for idRetornado in Ids:
                self.AtualizarRegistro('Sessoes','disponivel = 1',f'id = {idRetornado[0]}')
        except pyodbc.Error as e:
                print(f"Erro ao executar a consulta: {e}")
        
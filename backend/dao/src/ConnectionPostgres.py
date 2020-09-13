import psycopg2
from typing import NewType

user='postgres'
password='0P9O8i7u*_*'
host='localhost'
database='iacon'

class ConnectionPostgres():

    def __init__(self):
        self._connection: psycopg2.connect() = None

    #@staticmethod
    def getConnection(self):
        if self._connection is None:
            try:
                self._connection = psycopg2.connect(dsn=f"dbname={database} user={user} password={password} host={host}")
                # print('- Conexão feita com sucesso.')
            except Exception as e:
                print(f"** Não foi possível realizar a conexão. O erro é: {e}")
        return self._connection

    #@staticmethod
    def closeConnection(self):
        if self._connection is not None:
            try:
                self._connection.close()
                #print('- Conexão fechada com sucesso')
            except Exception as e:
                print(f"** Não foi possível fechar a conexão. O erro é: {e}")
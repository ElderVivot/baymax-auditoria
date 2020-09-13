from pymongo import MongoClient

class ConnectionMongo(object):
    def __init__(self, nameDB='iacon'):
        self._connection =  None
        self._selectDB = None
        self._nameDB = nameDB
        
    def getConnection(self):
        if self._connection is None:
            try:
                self._connection = MongoClient() # conecta num cliente do MongoDB rodando na sua máquina
                self._selectDB = self._connection[self._nameDB]
            except Exception as e:
                print(f"** Não foi possível realizar a conexão. O erro é: {e}")
        return self._selectDB

    def closeConnection(self):
        if self._connection is not None:
            try:
                self._connection.close()
                #print('- Conexão fechada com sucesso')
            except Exception as e:
                print(f"** Não foi possível fechar a conexão. O erro é: {e}")
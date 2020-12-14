import os
import sys
import pandas as pd
import json
from typing import Dict, List

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('fiscal')])

from dao.src.ConnectionODBC import ConnectionODBC
from utils.read_files.read_sql import readSql

class GetNoteDominio(object):
    def __init__(self):
        self._connectionODBC = ConnectionODBC()
        self._connection = self._connectionODBC.getConnection()
        self._data = None

    def get(self, codeCompanie: str, typeNote: str, numberNote: int, cgce: str) -> Dict:
        if typeNote == 'ser' and codeCompanie is not None:
            sql = readSql(absPath, 'get_note_dominio_servico.sql', int(codeCompanie), numberNote, cgce)
        elif typeNote == 'ent' and codeCompanie is not None:
            # don't has dateNote because in REST the date is date pagamento, and don't date emissao
            sql = readSql(absPath, 'get_note_dominio_entrada.sql', int(codeCompanie), numberNote, cgce)
        else:
            return

        try:
            df = pd.read_sql_query(sql, self._connection)
            data = json.loads(df.to_json(orient='records', date_format='iso'))
            self._data = data[0] if len(data) > 0 else None
        except Exception as e:
            print('error --> ', os.path.abspath(__file__), ' method get --> ', e)
        return self._data
    
    def closeConnection(self) -> None:
        self._connectionODBC.closeConnection()

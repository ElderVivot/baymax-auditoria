import os
import sys
import pandas as pd
import json
from typing import Dict, List

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('fiscal')])

from dao.src.ConnectionPostgres import ConnectionPostgres
from utils.read_files.read_sql import readSql

class GetCompanies(object):
    def __init__(self, dateStart: str, dateEnd: str):
        self._dateStart = dateStart
        self._dateEnd = dateEnd
        self._connectionPostgres = ConnectionPostgres()
        self._connection = self._connectionPostgres.getConnection()
        self._data = []

    def get(self, codeCompanie: str = '%', cgce: str = '%') -> List:
        sql = readSql(absPath, 'get_companies.sql', codeCompanie, self._dateStart, self._dateEnd, cgce)
        try:
            df = pd.read_sql_query(sql, self._connection)
            self._data = json.loads(df.to_json(orient='records', date_format='iso'))
        except Exception as e:
            print('error --> ', os.path.abspath(__file__), ' method get --> ', e)            
        return self._data if len(self._data) > 0 else None

    def closeConnection(self):
        self._connectionPostgres.closeConnection()
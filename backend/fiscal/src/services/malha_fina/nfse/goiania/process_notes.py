import os
import sys
import pandas as pd
import json
from typing import Dict, List

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('fiscal')])

from dao.src.ConnectionPostgres import ConnectionPostgres
from utils.read_files.read_sql import readSql
from get_note_dominio import GetNoteDominio
from get_companies import GetCompanies
from save_process import SaveProcess

class ProcessNotes(object):
    def __init__(self, dateStart: str, dateEnd: str):
        self._dateStart = dateStart
        self._dateEnd = dateEnd
        self._connectionPostgres = ConnectionPostgres()
        self._connection = self._connectionPostgres.getConnection()
        self._getNoteDominio = GetNoteDominio()
        self._getCompanies = GetCompanies(self._dateStart, self._dateEnd)
        self._saveProcess = SaveProcess()

    def get(self, codeCompanie: str = '%') -> List:
        sql = readSql(absPath, 'process_notes.sql', codeCompanie, self._dateStart, self._dateEnd)
        try:
            df = pd.read_sql_query(sql, self._connection)
            notes = json.loads(df.to_json(orient='records', date_format='iso'))
            for note in notes:
                noteDominioServico = self._getNoteDominio.get(
                    note['codeCompanie'], 'ser', note['numberNote'], note['cgceTomador'], note['dateNote'][0:10]
                )

                companieTomador = self._getCompanies.get(cgce=note['cgceTomador'])
                companieTomador = companieTomador[0] if companieTomador is not None else None
                codeCompanieTomador = companieTomador['code'] if companieTomador is not None else None
                noteDominioEntrada = self._getNoteDominio.get(
                    codeCompanieTomador, 'ent', note['numberNote'], note['cgceCompanie'], note['dateNote'][0:10]
                )

                self._saveProcess.save('ser', note, noteDominioServico, companieTomador)
        except Exception as e:
            print('error --> ', os.path.abspath(__file__), ' method get --> ', e)
    
    def closeConnection(self) -> None:
        self._getCompanies.closeConnection()
        self._getNoteDominio.closeConnection()
        self._connectionPostgres.closeConnection()

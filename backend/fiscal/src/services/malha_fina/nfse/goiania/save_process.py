import os
import sys
from datetime import datetime

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('fiscal')])

from dao.src.ConnectionMongo import ConnectionMongo

class SaveProcess(object):
    def __init__(self):
        self._connectionMongo = ConnectionMongo()
        self._connection = self._connectionMongo.getConnection()
        self._collection = self._connection['conferencia_notas_periodos']

    def makeDestinatario(self, companieTomador):
        if companieTomador is not None:
            destinatario = {
                "codigo": companieTomador['code'],
                "cgce": companieTomador['cgce']
            }
        else:
            destinatario = None

        return destinatario

    def getCodeCompaniePerTypeNote(self, typeNote, noteOriginal, companieTomador):
        codeCompanie = None
        if typeNote == 'ser':
            codeCompanie = noteOriginal['codeCompanie']
        if typeNote == 'ent' and companieTomador is not None:
            codeCompanie = companieTomador['code']
        return codeCompanie

    def checkIfNoteDominioIsCanceled(self, noteDominio):
        if noteDominio is None:
            return False
        if noteDominio['situacao'] == 2:
            return True
        return False

    def makeAlertas(self, noteOriginal, noteDominio):
        alertas = []
        if noteDominio is None:
            alertas.append(f"Nota fiscal {noteOriginal['numberNote']} não existe na Domínio.")
        return alertas

    def makeConferenciaNota(self, typeNote, noteOriginal, noteDominio, companieTomador):
        destinatario = self.makeDestinatario(companieTomador)

        codeCompanie = self.getCodeCompaniePerTypeNote(typeNote, noteOriginal, companieTomador)
        if codeCompanie is None: return None
        
        return {
            "empresa": codeCompanie,
            "arquivo": "",
            "processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "periodo": noteOriginal['dateNote'][:7],
            "numero": noteOriginal['numberNote'],
            "serie": '',
            "tipo": 0 if typeNote == 'ent' else 1,
            "modelo": 'NFS-e',
            "emitente": {
                "codigo": noteOriginal['codeCompanie'],
                "cnpj": noteOriginal['cgceCompanie']
            },
            "destinatario": destinatario,
            "dominio": 1 if noteDominio is not None else 0,
            "canc_arquivo": False if noteOriginal['statusNote'] == 'normal' else True,
            "canc_dominio": self.checkIfNoteDominioIsCanceled(noteDominio),
            "propria": False,
            "valor": noteOriginal['amountNote'],
            "alertas": self.makeAlertas(noteOriginal, noteDominio),
            "cfops": [],
            "desconhecimento": '',
            "chave": f"Nota {noteOriginal['numberNote']} - Tomador {companieTomador['cgce']} - Prestador {noteOriginal['cgceCompanie']}"
        }

    def save(self, typeNote, noteOriginal, noteDominio, companieTomador):
        try:
            conferencia_nota = self.makeConferenciaNota(typeNote, noteOriginal, noteDominio, companieTomador)
            if conferencia_nota is None: return # stop processing when None

            self._collection.update_one( 
                { 
                    "empresa": conferencia_nota['empresa'], 
                    "numero": conferencia_nota['numero'], 
                    "chave": conferencia_nota['chave'] 
                }, 
                { "$set": conferencia_nota}, 
                upsert=True 
            )
        except Exception as e:
            print('error --> ', os.path.abspath(__file__), ' method save --> ', e)  
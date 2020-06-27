import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
import json
import shutil
import csv
from fiscal.src.services.read_files.CallReadXmls import CallReadXmls
from api.Rest import ApiRest
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis

class Identifies_NFe_refNFe(object):
    def __init__(self):
        self._wayToRead = input('- Informe o caminho onde estão os XMLs que deseja ler: ').replace('\\', '/').replace('"', '')
        self._wayToSave = input('- Agora informe o caminho onde deseja salvar o arquivo CSV: ').replace('\\', '/').replace('"', '')
        self._filterDate = input('- A partir de qual data deseja organizar estes XMLs (dd/mm/aaaa): ')
        # self._wayToRead = "C:\\notas_fiscais\\modelo_55".replace('\\', '/').replace('"', '')
        # self._wayToSave = "C:\\notas_fiscais\\modelo_55".replace('\\', '/').replace('"', '')
        # self._filterDate = "01/01/2020"
        self._filterDate = funcoesUteis.retornaCampoComoData(self._filterDate)
        self._apiRest = ApiRest('extract_companies')
        self._companies = self._apiRest.get()

    def returnDataEmp(self, cgce):
        for companie in self._companies:
            cgceCompanie = funcoesUteis.treatTextField(companie["cgce_emp"])
            if cgceCompanie == "":
                continue

            if companie["cgce_emp"] == cgce:
                return companie

        return None
    
    def process(self, pathXml):
        callReadXmls = CallReadXmls(pathXml)
        nfs = callReadXmls.process()

        outputfile = open(os.path.join(self._wayToSave, 'notas_refnfe.csv'), 'w', encoding='utf-8')
        outputfile.write('Codigo Empresa;Numero Nota;Data Nota;Modelo;Serie;Valor;Valor ICMS;CNPJ Emitente;Nome Emitente;'
            'CNPJ Destinatario;Nome Destinatario;Chave Atual;Chave Referencial\n')

        if nfs is not None:
            for nf in nfs:
                refNFe = nf['refNFe']

                if refNFe != "":
                    cnpjIssuer = nf['cnpjIssuer']
                    companie = self.returnDataEmp(cnpjIssuer)

                    if companie is not None:
                        outputfile.write(f"{companie['codi_emp']};{nf['numberNF']};{nf['issueDateNF']};{nf['modelNF']};{nf['serieNF']};{nf['valueNF']};"
                            f"{nf['valueICMS']};'{cnpjIssuer};{nf['nameIssuer']};'{nf['cnpjReceiver']};{nf['nameReceiver']};"
                            f"'{nf['keyNF']};'{refNFe}\n")

        outputfile.close()

    def processAll(self):
        for root, dirs, files in os.walk(self._wayToRead):
            countFiles = len(files)
            for key, file in enumerate(files):
                wayFile = os.path.join(root, file)
                if file.lower().endswith(('.xml')):
                    print(f'- Processando XML {wayFile} / {key+1} de {countFiles}')
                    self.process(wayFile)

if __name__ == "__main__":
    obj = Identifies_NFe_refNFe()
    obj.processAll()

import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
import json
import shutil
from fiscal.src.services.read_files.CallReadXmls import CallReadXmls
from fiscal.src.services.rearrange_folder_xml.SaveXML import SaveXML
from api.Rest import ApiRest
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis

class RearrangeWayToSaveXML(object):
    def __init__(self):
        self._wayToRead = input('- Informe o caminho onde estão os XMLs que deseja organizar: ').replace('\\', '/').replace('"', '')
        self._wayToSave = input('- Agora informe o caminho onde deseja salvar os XMLs organizados: ').replace('\\', '/').replace('"', '')
        self._filterDate = input('- A partir de qual data deseja organizar estes XMLs (dd/mm/aaaa): ')
        # self._wayToRead = "C:\\notas_fiscais\\goiania\\2020-06-06_10-33-29_pm\\sucess\\73470384134".replace('\\', '/').replace('"', '')
        # self._wayToSave = "C:\\notas_fiscais".replace('\\', '/').replace('"', '')
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
        callReadXmls = CallReadXmls(pathXml, ['nfse_goiania'])
        nfs = callReadXmls.process()

        saveXML = SaveXML(self._wayToSave)

        if nfs is not None:

            for nf in nfs:
                # se tiver apenas uma nota retira o dado do xml pra poder em ver de fazer um write num xml fazer apenas um copy
                if len(nfs) == 1:
                    nf['xml'] = ''

                cgceIssuer = funcoesUteis.analyzeIfFieldIsValid(nf, 'cgceIssuer')
                cgceReceiver = funcoesUteis.analyzeIfFieldIsValid(nf, 'cgceReceiver')
                issueDate = funcoesUteis.analyzeIfFieldIsValid(nf, 'issueDateNF', None)

                if issueDate < self._filterDate:
                    continue

                companieIssuer = self.returnDataEmp(cgceIssuer)
                companieReceiver = self.returnDataEmp(cgceReceiver)

                if companieIssuer is not None:
                    nf['companie'] = companieIssuer
                    nf['typeNF'] = 'Saidas'

                    saveXML.save(nf, pathXml)

                if companieReceiver is not None:
                    nf['companie'] = companieReceiver
                    nf['typeNF'] = 'Entradas'

                    saveXML.save(nf, pathXml)

    def processAll(self):
        for root, dirs, files in os.walk(self._wayToRead):
            countFiles = len(files)
            for key, file in enumerate(files):
                wayFile = os.path.join(root, file)
                if file.lower().endswith(('.xml')):
                    print(f'- Processando XML {wayFile} / {key+1} de {countFiles}')
                    self.process(wayFile)

if __name__ == "__main__":
    rearrangeWayToSaveXML = RearrangeWayToSaveXML()
    rearrangeWayToSaveXML.processAll()

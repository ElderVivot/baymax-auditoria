import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis


class NFe(object):
    def __init__(self, dataXml):
        self._dataXml = dataXml
        self._nfs = []

    def readNFe(self):
        objNF = {}

        keyNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        keyNF = keyNF[3:]
        objNF['keyNF'] = keyNF
        
        numberNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'nNF'])
        objNF['numberNF'] = numberNF
        
        issueDateNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'dhEmi'])
        issueDateNF2 = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'dEmi'])
        issueDateNF = issueDateNF2 if ( issueDateNF == "" or issueDateNF is None ) else issueDateNF
        issueDateNF = funcoesUteis.transformDateFieldToString(funcoesUteis.retornaCampoComoData(issueDateNF, 2))
        objNF['issueDateNF'] = issueDateNF

        modelNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'mod'])
        objNF['modelNF'] = modelNF

        serieNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'serie'])
        objNF['serieNF'] = serieNF

        valueNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'total', 'ICMSTot', 'vNF'])
        objNF['valueNF'] = valueNF

        valueICMS = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'total', 'ICMSTot', 'vICMS'])
        objNF['valueICMS'] = valueICMS

        refNFe = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'NFref', 'refNFe'])
        objNF['refNFe'] = refNFe

        nameIssuer = funcoesUteis.justLettersNumbersDots(funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'xNome']))
        nameReceiver = funcoesUteis.justLettersNumbersDots(funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'xNome']))

        typeNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'tpNF'])
        
        cnpjIssuer = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'CNPJ'])
        cpfIssuer = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'CPF'])
        cnpjIssuer = cpfIssuer if cnpjIssuer == "" else cnpjIssuer
        
        cnpjReceiver = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'CNPJ'])
        cpfReceiver = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'CPF'])
        cnpjReceiver = cpfReceiver if cnpjReceiver == "" else cnpjReceiver

        if typeNF == "0": # quem emitiu foi quem comprou a nota, então o dest vira o emit (nota própria)
            cnpjIssuerCorrect = cnpjReceiver
            nameIssuerCorrect = nameReceiver
            cnpjReceiverCorrect = cnpjIssuer
            nameReceiverCorrect = nameIssuer
        else:
            cnpjIssuerCorrect = cnpjIssuer
            nameIssuerCorrect = nameIssuer
            cnpjReceiverCorrect = cnpjReceiver
            nameReceiverCorrect = nameReceiver

        objNF['cnpjIssuer'] = cnpjIssuerCorrect
        objNF['nameIssuer'] = nameIssuerCorrect
        objNF['cnpjReceiver'] = cnpjReceiverCorrect
        objNF['nameReceiver'] = nameReceiverCorrect

        # produtos = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'det'])
        # objNF['produtos'] = produtos

        self._nfs.append(objNF)

        return self._nfs


if __name__ == "__main__":
    dataXml = readXml("C:/notas_fiscais/modelo_55/52191006314327000203550010057739601112482590.xml")

    # with open("C:/_temp/notas_gyn_teste/04605182000185.xml") as file:
    #     data = xmldict.parse(file.read())
    #     print(xmldict.unparse(data))

    nf = NFe(dataXml)
    print(nf.readNFe())
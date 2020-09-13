import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis
import xmltodict as xmldict
from collections import OrderedDict


class NFSeGoiania(object):
    def __init__(self, dataXml):
        self._dataXml = dataXml
        self._nfs = []

    def readNFe(self):
        nfs = []

        nfsXml = funcoesUteis.returnDataFieldInDict(self._dataXml, ['geral', 'GerarNfseResposta'])

        if type(nfsXml) is not list:
            nfs.append(nfsXml)
        else:
            nfs = nfsXml

        for nf in nfs:
            nfsConvertToXml = OrderedDict()
            
            nfsConvertToXml['GerarNfseResposta'] = nf
            nfsConvertToXml = xmldict.unparse(nfsConvertToXml)
            nfsConvertToXml = funcoesUteis.removerAcentosECaracteresEspeciais(nfsConvertToXml)
            
            objNF = {}
             
            objNF['numberNF'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'Numero'])

            objNF['keyNF'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'CodigoVerificacao'])
            objNF['keyNF'] = f"{objNF['numberNF']}-{objNF['keyNF']}"

            objNF['issueDateNF'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'DataEmissao'])
            objNF['issueDateNF'] = funcoesUteis.retornaCampoComoData(objNF['issueDateNF'], 2)

            objNF['valueNF'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'DeclaracaoPrestacaoServico', 'InfDeclaracaoPrestacaoServico', 'Servico', 'Valores', 'ValorServicos'])
            
            objNF['cnpjIssuer'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'DeclaracaoPrestacaoServico', 'InfDeclaracaoPrestacaoServico', 'Prestador', 'CpfCnpj', 'Cnpj'])
            objNF['cpfIssuer'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'DeclaracaoPrestacaoServico', 'InfDeclaracaoPrestacaoServico', 'Prestador', 'CpfCnpj', 'Cpf'])
            objNF['cgceIssuer'] = objNF['cpfIssuer'] if objNF['cnpjIssuer'] == "" else objNF['cnpjIssuer']
            
            objNF['cnpjReceiver'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'DeclaracaoPrestacaoServico', 'InfDeclaracaoPrestacaoServico', 'Tomador', 'IdentificacaoTomador', 'CpfCnpj', 'Cnpj'])
            objNF['cpfReceiver'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'DeclaracaoPrestacaoServico', 'InfDeclaracaoPrestacaoServico', 'Tomador', 'IdentificacaoTomador', 'CpfCnpj', 'Cpf'])
            objNF['cgceReceiver'] = objNF['cpfReceiver'] if objNF['cnpjReceiver'] == "" else objNF['cnpjReceiver']

            objNF['statusNF'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaMensagemRetorno', 'MensagemRetorno', 'Mensagem'])

            objNF['modelNF'] = 'NFS-e'

            objNF['xml'] = nfsConvertToXml

            self._nfs.append(objNF)

        return self._nfs


if __name__ == "__main__":
    dataXml = readXml("C:/_temp/notas_gyn_teste/18040800000100.xml")#04605182000185 18040800000100

    # with open("C:/_temp/notas_gyn_teste/04605182000185.xml") as file:
    #     data = xmldict.parse(file.read())
    #     print(xmldict.unparse(data))

    nf = NFSeGoiania(dataXml)
    print(nf.readNFe())
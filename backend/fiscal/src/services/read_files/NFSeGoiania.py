import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis


class NFSeGoiania(object):
    def __init__(self, dataXml):
        self._dataXml = dataXml
        self._nfs = []

    def readNFe(self):
        nfsXml = funcoesUteis.returnDataFieldInDict(self._dataXml, ['geral', 'GerarNfseResposta'])

        for nf in nfsXml:
            objNF = {}

            objNF['keyNF'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'CodigoVerificacao'])
            
            objNF['numberNF'] = funcoesUteis.returnDataFieldInDict(nf, ['ListaNfse', 'CompNfse', 'Nfse', 'InfNfse', 'Numero'])

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

            self._nfs.append(objNF)

        return self._nfs


if __name__ == "__main__":
    dataXml = readXml("C:/_temp/notas_gyn_teste/04605182000185.xml")

    nf = NFSeGoiania(dataXml)
    print(nf.readNFe())
import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis
from fiscal.src.services.read_files.NFe import NFe
from fiscal.src.services.read_files.NFeCanceled import NFeCanceled
from fiscal.src.services.read_files.NFSeGoiania import NFSeGoiania


class CallReadXmls(object):
    def __init__(self, xml, filterTypeNFs=['nfe', 'nfse_goiania']):
        self._xml = xml
        self._filterTypeNFs = filterTypeNFs

    def process(self):
        dataXml = readXml(self._xml)

        isNFe = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        isNFeCanceled = funcoesUteis.returnDataFieldInDict(dataXml, ['procEventoNFe', 'evento', 'infEvento', 'chNFe'])
        isNFSeGoiania = funcoesUteis.returnDataFieldInDict(dataXml, ['geral', 'GerarNfseResposta'])

        nf = None

        if isNFe != "" and self._filterTypeNFs.count('nfe') > 0:
            nfe = NFe(dataXml)
            nf = nfe.readNFe()

        if isNFeCanceled != "" and self._filterTypeNFs.count('nfe') > 0:
            nfeCanceled = NFeCanceled(dataXml)
            nf = nfeCanceled.readNFeCanceled()

        if isNFSeGoiania != "" and self._filterTypeNFs.count('nfse_goiania') > 0:
            nfseGoiania = NFSeGoiania(dataXml)
            nf = nfseGoiania.readNFe()

        return nf


# if __name__ == "__main__":
#     callReadXmls = CallReadXmls('C:/_temp/notas_mirene/52190505452064000490550010000065851000065850.xml')
#     nf = callReadXmls.process()
#     print(nf)
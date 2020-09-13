import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import shutil
import tools.funcoesUteis as funcoesUteis

class SaveXML(object):
    def __init__(self, wayBase):
        self._wayBase = wayBase

    def save(self, dataNF, wayXml):
        wayToSaveXml = os.path.join(self._wayBase, f"{dataNF['companie']['nome_emp'][:70]} - {str(dataNF['companie']['codi_emp'])}", \
            f"{dataNF['issueDateNF'].year}", f"{dataNF['issueDateNF'].month:0>2}", f"{dataNF['typeNF']}", f"{dataNF['modelNF']}")
        
        if os.path.exists(wayToSaveXml) is False:
            os.makedirs(wayToSaveXml)

        pathNewXml = os.path.join(wayToSaveXml, f"{dataNF['keyNF']}.xml")

        try:
            # se não tiver dados do xml no objeto de nota então apenas copia o xml pra nova pasta
            if dataNF['xml'] == '':
                shutil.copy(wayXml, pathNewXml)
            else:
                with open(pathNewXml, 'w', encoding='utf-8') as xml:
                    xml.write(dataNF['xml'])
        except Exception:
            pass        
        
        print(f"\t- É uma nota de {dataNF['typeNF']} - {dataNF['modelNF']} da empresa {dataNF['companie']['codi_emp']}.")
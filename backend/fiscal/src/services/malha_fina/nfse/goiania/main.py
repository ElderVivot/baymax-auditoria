from get_companies import GetCompanies
from process_notes import ProcessNotes
import sys
import calendar

class MainMalhaFinaGoiania(object):
    def __init__(self, dateStart: str, dateEnd: str, codeCompanie: str = '%'):
        self._dateStart = dateStart
        self._dateEnd = dateEnd
        self._codeCompanie = codeCompanie
        self._getCompanies = GetCompanies(self._dateStart, self._dateEnd)
        self._processNotes = ProcessNotes(self._dateStart, self._dateEnd)

    def process(self):
        companies = self._getCompanies.get(self._codeCompanie)
        self._getCompanies.closeConnection()
        
        for companie in companies:
            print(f"- Processando empresa {companie['code']} - {companie['name']}")
            self._processNotes.get(companie['dateinicialasclient'], companie['datefinalasclient'], companie['code'])

        self._processNotes.closeConnection()

if __name__ == "__main__":
    codeCompanie = str(sys.argv[1])
    monthInicial = int(sys.argv[2])
    yearInicial = int(sys.argv[3])
    monthFinal = int(sys.argv[4])
    yearFinal = int(sys.argv[5])

    dayFinal = calendar.monthrange(yearFinal, monthFinal)[1]

    dateInicial = f'{yearInicial}-{monthInicial:0>2}-01'
    dateFinal = f'{yearFinal}-{monthFinal:0>2}-{dayFinal:0>2}'

    mainMalhaFinaGoiania = MainMalhaFinaGoiania(dateInicial, dateFinal, codeCompanie)
    mainMalhaFinaGoiania.process()
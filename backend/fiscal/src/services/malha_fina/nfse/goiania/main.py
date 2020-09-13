from get_companies import GetCompanies
from process_notes import ProcessNotes

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
            self._processNotes.get(companie['code'])

        self._processNotes.closeConnection()

if __name__ == "__main__":
    mainMalhaFinaGoiania = MainMalhaFinaGoiania('2020-01-01', '2020-12-01')
    mainMalhaFinaGoiania.process()
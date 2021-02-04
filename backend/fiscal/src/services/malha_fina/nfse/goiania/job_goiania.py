from pytz import utc
import calendar
from apscheduler.schedulers.blocking import BlockingScheduler
from main import MainMalhaFinaGoiania

def instantiateObject():
    codeCompanie = '%'
    monthInicial = 1
    yearInicial = 2020
    monthFinal = 12
    yearFinal = 2021

    dayFinal = calendar.monthrange(yearFinal, monthFinal)[1]

    dateInicial = f'{yearInicial}-{monthInicial:0>2}-01'
    dateFinal = f'{yearFinal}-{monthFinal:0>2}-{dayFinal:0>2}'

    mainMalhaFinaGoiania = MainMalhaFinaGoiania(dateInicial, dateFinal, codeCompanie)
    mainMalhaFinaGoiania.process()

scheduler = BlockingScheduler(timezone=utc)
scheduler.add_job(instantiateObject, 'interval', hours=6)
scheduler.start()
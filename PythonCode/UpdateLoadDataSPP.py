# Update historical SPP load data

from datetime import date
from datetime import datetime, timedelta
import pandas as pd
import os

dfHistLoad = pd.read_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Load/History/HistLoadSPP.csv')
dfHistLoad['MarketHour'] = pd.to_datetime(dfHistLoad['MarketHour'])

lastDay = max(dfHistLoad['MarketHour']).date()
for day in pd.date_range(lastDay.strftime("%m/%d/%Y"), date.today().strftime("%m/%d/%Y")):
    try:
        dfTemp = pd.read_csv('https://marketplace.spp.org/file-browser-api/download/hourly-load?path=%2F' + str(day.year) + '%2FDAILY_HOURLY_LOAD-' + str(day.strftime("%Y%m%d")) + '.csv')   
        dfTemp.columns = dfTemp.columns.str.replace(' ', '')
        dfTemp['MarketHour'] = pd.to_datetime(dfTemp['MarketHour']) - timedelta(hours=7) # convert from GMT to CST, get data in hour beginning
        dfHistLoad = pd.concat([dfHistLoad, dfTemp])
    except:
        print('Missing historical load data for ' + str(day))

dfHistLoad = dfHistLoad.round(decimals=2)
dfHistLoad.to_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Load/History/HistLoadSPP.csv', index=False)
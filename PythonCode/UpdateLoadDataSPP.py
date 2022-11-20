# Update historical SPP load data

from datetime import date
import datetime
import pandas as pd

dfHistLoad = pd.read_csv('C:/Users/bwill/Documents/RainShine/Data/Load/History/HistLoadSPP.csv')
dfHistLoad['MarketHour'] = pd.to_datetime(dfHistLoad['MarketHour'])

lastDay = max(dfHistLoad['MarketHour']).date()
for day in pd.date_range(lastDay.strftime("%m/%d/%Y"), date.today().strftime("%m/%d/%Y")):
    try:
        dfTemp = pd.read_csv('https://marketplace.spp.org/file-browser-api/download/hourly-load?path=%2F' + str(day.year) + '%2FDAILY_HOURLY_LOAD-' + str(day.strftime("%Y%m%d")) + '.csv')   
        dfTemp.columns = dfTemp.columns.str.replace(' ', '')
        dfTemp['MarketHour'] = pd.to_datetime(dfTemp['MarketHour'])
        dfHistLoad = pd.concat([dfHistLoad, dfTemp])
    except:
        print('Missing historical load data for ' + str(day))

dfHistLoad = dfHistLoad.round(decimals=2)
dfHistLoad.to_csv('C:/Users/bwill/Documents/RainShine/Data/Load/History/HistLoadSPP.csv', index=False)
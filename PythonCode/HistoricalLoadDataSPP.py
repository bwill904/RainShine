# Meant to be ran once, grabbing long term historical data from SPP
import pandas as pd
import os
from datetime import timedelta

strHistLoadDir = 'C:/Users/bwill/Documents/RainShine/Data/Load/History/SPP'
for year in os.listdir(strHistLoadDir):
    for monthFile in os.listdir(strHistLoadDir + '/' + year):
        dfTemp = pd.read_csv(strHistLoadDir + '/' + year + '/' + monthFile)
        dfTemp.columns = dfTemp.columns.str.replace(' ', '')
        if year == os.listdir(strHistLoadDir)[0] and monthFile == os.listdir(strHistLoadDir + '/' + year)[0]:
            dfHistLoad = dfTemp
        else: dfHistLoad = pd.concat([dfHistLoad, dfTemp])

dfHistLoad['MarketHour'] = pd.to_datetime(dfHistLoad['MarketHour']) - timedelta(hours=7) # convert from GMT to CST, get data in hour beginning
dfHistLoad = dfHistLoad.round(decimals=2)
dfHistLoad.to_csv('C:/Users/bwill/Documents/RainShine/Data/Load/History/HistLoadSPP.csv', index=False)

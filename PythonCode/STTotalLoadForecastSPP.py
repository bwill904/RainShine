# Pulling short-term total load forecast data from SPP

import pandas as pd
from datetime import datetime, timedelta

dfForLoad = pd.read_csv('https://marketplace.spp.org/chart-api/load-forecast/asFile')

dfForLoad = dfForLoad[['Interval', 'MTLF']].sort_values('Interval') # time already in CST
dfForLoad['Interval'] = pd.to_datetime(dfForLoad['Interval'])
dfForLoad = dfForLoad.dropna()
dfForLoad['HourBeginning'] = dfForLoad['Interval'].dt.hour
dfForLoad = dfForLoad.rename(columns={'Interval':'MarketHour', 'MTLF':'TotalLoad'})

# getting historical load data and zone names
dfHistLoad = pd.read_csv('C:/Users/bwill/Documents/RainShine/Data/Load/History/HistLoadSPP.csv')
dfHistLoad['MarketHour'] = pd.to_datetime(dfHistLoad['MarketHour'])
vecZones = dfHistLoad.columns.values.tolist()
vecZones.remove('MarketHour')

zoneLoadModel = 'prevDay'
# using previous day for zonal load forecast
if (zoneLoadModel == 'prevDay')
    dfRecentLoad = dfHistLoad[dfHistLoad['MarketHour'].dt.date == max(dfHistLoad['MarketHour'].dt.date)]
    if (len(dfRecentLoad) != 24): # if we don't have full day for most recent historical date
        dfRecentLoad = dfHistLoad[dfHistLoad['MarketHour'].dt.date == max(dfHistLoad['MarketHour'].dt.date - timedelta(days=1))]
    
    # calculating hourly percentages of total load for each zone
    dfRecentLoad['TotalLoad'] = dfRecentLoad.iloc[vecZones].sum(axis=1)
    dfRecentLoad = dfRecentLoad.reset_index()
    dfRecentLoad = dfRecentLoad.melt(id_vars=['MarketHour', 'Total'], value_vars = vecZones, var_name = 'ZoneName', value_name = 'ZoneLoad')
    dfRecentLoad['ZoneLoadPercent'] = dfRecentLoad['ZoneLoad'] / dfRecentLoad['Total']
    dfRecentLoad['HourBeginning'] = dfRecentLoad['MarketHour'].dt.hour
    dfRecentLoad = dfRecentLoad.drop(columns=['MarketHour', 'Total', 'ZoneLoad'])

    output = dfForLoad.merge(dfRecentLoad, on='HourBeginning', how='outer')



    test = test.pivot(index='MarketHour', columns='ZoneName', ZoneLoad)

    dfForLoad.to_csv('C:/Users/bwill/Documents/RainShine/Data/Load/Forecast/SPP/ForLoadSPP ' + str(min(dfForLoad['MarketHour']).strftime('%Y-%m-%d %H')) + '.csv', index=False)
# script to pulll historical weather data

import pandas as pd
import os
import pickle
import time
from datetime import datetime 
from meteostat import Stations, Point, Daily, Hourly

dfStations = pd.read_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Stations.csv')

for state in dfStations.region.unique():
    dfStationsState = dfStations[dfStations['region'] == state]
    if 'Hourly-' + state + '.pkl' in os.listdir(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History'): 
        continue # don't write data if already there
    else: time.sleep(20) # take a break to avoid overquerying
    dHourly = {}
    for stationId in dfStationsState.id.unique():
        dfTemp = Hourly(stationId, datetime(2010, 1, 1), datetime(2022, 12, 31, 23, 59))
        dfTemp = dfTemp.fetch()
        dHourly[stationId] = dfTemp
    # dHourly.to_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Stations.csv', index=False)
    with open(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Hourly-' + state + '.pkl', 'wb') as f:
        pickle.dump(dHourly, f)
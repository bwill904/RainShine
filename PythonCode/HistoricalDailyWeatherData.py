# script to pulll historical weather data

import pandas as pd
import os
import pickle
import time
from datetime import datetime 
from meteostat import Stations, Point, Daily

dfStations = pd.read_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Stations.csv')

for state in dfStations.region.unique():
    dfStationsState = dfStations[dfStations['region'] == state]
    if 'Daily-' + state + '.pkl' in os.listdir(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Daily'): 
        continue # don't write data if already there
    else: time.sleep(20) # take a break to avoid overquerying
    dDaily = {}
    for stationId in dfStationsState.id.unique():
        dfTemp = Daily(stationId, datetime(1993, 1, 1), datetime(2022, 12, 31, 23, 59))
        dfTemp = dfTemp.fetch()
        dDaily[stationId] = dfTemp
    with open(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Daily/Daily-' + state + '.pkl', 'wb') as f:
        pickle.dump(dDaily, f)
# script to pulll historical weather data

import pandas as pd
import os
import pickle
import time
from datetime import datetime 
from meteostat import Stations, Point, Hourly

dfStations = pd.read_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Stations.csv')

for state in dfStations.region.unique():
    dfStationState = dfStations[dfStations['region'] == state]
    for stationId in dfStationState.id.unique():
        if 'Hourly-' + state + "-" + stationId + '.pkl' in os.listdir(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Hourly'): 
            continue # don't write data if already there
        else: 
            time.sleep(10) # take a break to avoid overquerying
            dfTemp = Hourly(stationId, datetime(2000, 1, 1), datetime(2022, 12, 31, 23, 59))
            dfTemp = dfTemp.fetch()
            with open(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Hourly/Hourly-' + state + "-" + stationId + '.pkl', 'wb') as f:
                pickle.dump(dfTemp, f)
# script to pulll historical weather data

import pandas as pd
import os
from meteostat import Stations, Point, Daily, Hourly

stations = Stations().region('US')
dfStations = stations.fetch(10000)
dfStations = dfStations.dropna(subset = ["region", "hourly_start", "daily_start"])

# get 10 best stations for each state, may need to change this in the future
for state in dfStations.region.unique():
    numStations = dfStations[dfStations["region"] == state].shape[0]
    vecRemoveStations = dfStations[dfStations["region"] == state].sort_values("hourly_start").tail(numStations - 10).icao.tolist()
    dfStations = dfStations[~dfStations["icao"].isin(vecRemoveStations)]

dfStations.to_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Stations.csv', index=False)
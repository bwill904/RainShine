# script to pulll historical weather data

import pandas as pd
import os
from meteostat import Stations, Point, Daily, Hourly

dfStations = pd.read_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Stations.csv')

for station in dfStations.icao.unique():


stations = Stations().region('US')
dfStations = stations.fetch(10000)
dfStations = dfStations.dropna(subset = ["region", "hourly_start", "daily_start"])

dfStations.to_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Stations.csv', index=False)
# script to pulll historical weather data

import pandas as pd
import os
import time
from datetime import datetime 
from meteostat import Stations, Point, Daily, Hourly

# pull historical weather stations
def weatherStations():
    stations = Stations().region('US')
    dfStations = stations.fetch(10000)
    dfStations.reset_index(inplace = True)
    dfStations['id'] = dfStations['id'].astype('str')
    dfStations = dfStations.dropna(subset = ["region", "hourly_start", "daily_start"])

    dfStations = dfStations[~dfStations.region.isin(['RO', 'SA', 'WQ', 'HI', 'AK'])] # just mainland US

    # # get 10 best stations, may need to change this in the future
    # for state in dfStations.region.unique():
    #     numStations = dfRemoveStations.shape[0]
    #     dfRemoveStations = dfStations[dfStations["region"] == state]
    #     vecRemoveStations = dfRemoveStations.sort_values("hourly_start").tail(numStations - 10).icao.tolist()
    #     dfStations = dfStations[~dfStations["icao"].isin(vecRemoveStations)]
    
    return(dfStations)

# pull historical weather data
def histWeather(dfStations, granularity):
    dOutput = {}

    for stationId in dfStations.id.unique():
        if granularity == 'daily':
            dfTemp = Daily(stationId, datetime(1993, 1, 1), datetime(2022, 12, 31, 23, 59))
        elif granularity == 'hourly':
            dfTemp = Hourly(stationId, datetime(2000, 1, 1), datetime(2022, 12, 31, 23, 59))
        dfTemp = dfTemp.fetch()
        time.sleep(10) # take a break to avoid overquerying

        dOutput[stationId] = dfTemp
    return(dOutput)



import pandas as pd
import pickle
import os

dfStation = pd.read_csv(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Stations.csv')

for state in dfStation.region.unique():
    vecHourlyFiles = os.listdir(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Hourly')
    vecHourlyFiles = list(filter(lambda x: state in x, vecHourlyFiles))
    for file in vecHourlyFiles:
        with open(os.path.expanduser('~/Documents') + '/RainShine/Data/Weather/History/Hourly/' + file, 'rb') as f:
            dfData = pickle.load(f)
        dfData = pickle.load(f)


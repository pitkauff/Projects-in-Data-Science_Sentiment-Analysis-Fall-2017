# coding: utf-8

# In[14]:

############### READ ME ##############################
# usage: 
# input (default values show): augmentWeather(start_year=2017,end_year=2017,stationID='725030-14732',location_name='manhattan', root_path='../../')
# output: json file saved in data directory "locationName_weather.json"
# output: returns DataFrame of the same data

# stationID='998479-99999',location_name='sanFrancisco'
# stationID='725030-14732',location_name='manhattan'
#####################################################


# In[15]:
import json

import math

from scripts.enrich.weather import getNewWeather
from scripts.utils import utils


def getWeatherAtDatetime(created_at, weather):
    from datetime import datetime
    d = str(int(created_at))
    d = int(d[:10])
    tweet_year = datetime.fromtimestamp(d).strftime('%Y')
    tweet_month = datetime.fromtimestamp(d).strftime('%m')
    tweet_day = datetime.fromtimestamp(d).strftime('%d')
    tweet_hour = int(datetime.fromtimestamp(d).strftime('%I'))

    weatherKey = tweet_year + '-' + tweet_month + '-' + tweet_day
    weatherDataDaily = weather[weatherKey]['data']
    weatherDataHourly = weatherDataDaily[tweet_hour]
    return weatherDataHourly


# In[16]:

def enrichWithWeather(location_name, coordinates):
    actualCityNameMap = {
        'chicago': 'chicago',
        'asburyPark': 'asburyPark',
        'denver': 'denver',
        'detroit': 'detroit',
        'houston': 'houston',
        'nyc': 'manhattan',
        'Phoenix': 'phoenix',
        'sanFrancisco': 'sanFrancisco',
        'seattle': 'seattle',
    }
    locationWeatherDictionary = {}
    print 'Getting weather data'
    if type(coordinates) == str:
        # weather = None
        weather = getNewWeather.getWeatherForCoordinates(coordinates)
        locationWeatherDictionary[location_name] = weather
    else:
        for place, coordinate in coordinates.iteritems():
            weather = getNewWeather.getWeatherForCoordinates(coordinate)
            # weather = None
            locationWeatherDictionary[place] = weather

    dataFilePath = utils.getFullPathFromDataFileName(location_name + '.json')
    with open(dataFilePath) as data_file:
        jsonData = json.load(data_file)
        print 'Adding weather to data of length = ' + str(len(jsonData))

        count = 0
        for dataObject in jsonData:
            if count % 100000 == 0:
                print "Adding weather data: ", count
            count = count + 1

            datetime = dataObject['created']
            city_ = dataObject['city']
            try:
                place = actualCityNameMap[city_]
                weather = locationWeatherDictionary[place]
                tweetWeather = getWeatherAtDatetime(datetime, weather)

                dataObject.update(tweetWeather)
            except:
                print city_

        outputPath = utils.getFullPathFromDataFileName(location_name + '_weather.json')
        print 'Saving file: ', outputPath
        with open(outputPath, 'w') as outfile:
            json.dump(jsonData, outfile)

    print 'Saved file: ', outputPath

    return outputPath

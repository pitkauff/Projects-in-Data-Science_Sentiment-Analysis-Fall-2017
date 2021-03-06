import numpy as np
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingRegressor

from scripts.learn import machineLearning
from scripts.learn.machineLearning import tuneNValue

# ______________________________________________________
# HOW LONG WILL MY CLASSIFIER TAKE TO RUN ON MY MACHINE?
# ______________________________________________________
#
# Create a basic classifier
classifier = BaggingRegressor(random_state=43)
classifierName = "BaggingRegressor"  # No spaces, this will be a file name

# Add the names of all data files you want to use to this list
jsonFileNames = [
    'chicago_weather_sentiment_clean_grouped.json',
    'denver_weather_sentiment_clean_grouped.json',
    'detroit_weather_sentiment_clean_grouped.json',
    'houston_weather_sentiment_clean_grouped.json',
    'manhattan_weather_sentiment_clean_grouped.json',
    'phoenix_weather_sentiment_clean_grouped.json',
    'sanFrancisco_weather_sentiment_clean_grouped.json',
    'seattle_weather_sentiment_clean_grouped.json',
]


# We want to see how long it will take to train our classifier
# This will make a file called <classifierName>_number_data_points.csv
def tuneBaggingNValues():
    nValues = [
        2 ** 4,
        2 ** 5,
        2 ** 6,
        2 ** 7,
        2 ** 8,
        2 ** 9,
        2 ** 10,
        1598,
        2 ** 11,
        2 ** 12,
        2 ** 13,
    ]

    tuneNValue(nValues, classifier, classifierName, jsonFileNames)


# ______________________________________________________
# WHAT ARE THcountE BEST VALUES OF EACH PARAMETER?
# ______________________________________________________
#
    # This should be a list of all your parameters with a wide range of possible values
def tuneBaggingParametersIndividually(decentNValues):
    parameterGrid = {
        'n_estimators': np.arange(10,500,40),
        'max_samples': [100],
        'max_features': [5, 10],
        'bootstrap': [True],
        'bootstrap_features': [True],
        'warm_start': [True],
    }

    threeBestParams = machineLearning.tuneParametersIndividually(parameterGrid, classifierName, classifier,
                                                                 jsonFileNames,
                                                                 decentNValue, 2)
    return threeBestParams


# ______________________________________________________
# WHAT IS THE BEST COMBINATION OF VARIABLES?
# ______________________________________________________
#

# Fill this grid with only the best parameter values, as every single combination will be run
def tuneBaggingParameters(decentNValues, parameterGrid):
    parameterGrid = {
    'n_estimators': np.arange(10,500,40),
    'max_samples': [100],
    'max_features': [10,5],
    'bootstrap': [True],
    'bootstrap_features': [True],
    'warm_start': [True],
    }


    bestParams = machineLearning.tuneParameters(parameterGrid, classifierName, classifier, jsonFileNames, decentNValue)
    return bestParams


# ______________________________________________________
# RUN THE MODEL WITH BEST PARAMETERS
# ______________________________________________________
#
def runFineTunedBagging():
    bestRegressor = BaggingRegressor(
        n_estimators=100,
        max_samples=100,
        max_features=5,
        bootstrap=True,
        bootstrap_features=True,
        warm_start=True
    )

    machineLearning.runRegressor(bestRegressor, "bagging", jsonFileNames)


tuneBaggingNValues()

# Pick a reasonable n value considering you'll be training the model a few hundred times
# We want an n with a high accuracy but low run time
decentNValue = 2000

bestParams = tuneBaggingParametersIndividually(decentNValue)
print ''
print ''
print 'here are all possible best parameters'
print bestParams
print ''
print ''

bestParams = tuneBaggingParameters(decentNValue, bestParams)
print ''
print ''
print 'here are actual best parameters'
print bestParams


runFineTunedBagging()



from flask_restful import Resource
import json
import utils as Utils
import os
from config import trained_models_dir_path
import csv
import threading
import statistics
import json
import numpy
import datetime
from flask import jsonify

class Model_Statistics:
    def __init__(self):
        self.date = []
        self.consumption = []
        self.coal = []
        self.gas = [] 
        self.hidroelectric = []
        self.nuclear = []
        self.wind = []
        self.solar = []
        self.biomass = []
        self.production = []
        self.dataCount = 0

    def push(self, date, consumption, coal, gas, hidroelectric, nuclear, wind, solar, biomass, production):
        self.dataCount += 1
        self.date.append(int(date))
        self.consumption.append(float(consumption))
        self.coal.append(float(coal))
        self.gas.append(float(gas)) 
        self.hidroelectric.append(float(hidroelectric))
        self.nuclear.append(float(nuclear))
        self.wind.append(float(wind))
        self.solar.append(float(solar))
        self.biomass.append(float(biomass))
        self.production.append(float(production))

    def getArrayForKeys(self):
        return self.__dict__

class Statistics():
    def __init__(self, stats_cache_path):
        self.stats_cache_path = stats_cache_path

    def readCachedStatistics(self):
        cacheFile = open(self.stats_cache_path, "r")
        cachedContent = cacheFile.read()
        return cachedContent

    def writeStatisticsCache(self, cachedContent):
        cacheFile = open(self.stats_cache_path, "w")
        cacheFile.write(cachedContent)

    def deleteCachedStatistics(self):
        cacheFile = open(self.stats_cache_path, "w")
        cacheFile.write('')
        
    def buildDictionaryStats(self, data, keys):
        for key in keys:
            resultsDictionary = dict()
            resultsDictionary['sum'] = sum(data[key])
            resultsDictionary['min'] = min(data[key])
            resultsDictionary['max'] = max(data[key])
            resultsDictionary['avg'] = numpy.mean(data[key])
            resultsDictionary['data'] = self.findGoodSubset(data[key], 1000)
            resultsDictionary['stdDev'] = numpy.std(data[key])
            data[key] = resultsDictionary
        
        return data

    def extractMonthlyData(self, data):
        dataDict = data.getArrayForKeys()
        resultsDictionary = dict()

        for index in range(0, dataDict["dataCount"]):
            dateObject = datetime.datetime.fromtimestamp(dataDict["date"][index])
            if dateObject.month not in resultsDictionary.keys():
                resultsDictionary[dateObject.month] = dict()
            for key in dataDict.keys():
                if key == "dataCount" or key == "date":
                    continue
                if key not in resultsDictionary[dateObject.month]:
                    resultsDictionary[dateObject.month][key] = []
                resultsDictionary[dateObject.month][key].append(dataDict[key][index])

        for index in range(1, 13):
            resultsDictionary[index] = self.buildDictionaryStats(resultsDictionary[index], resultsDictionary[index].keys())

        return resultsDictionary

    def findGoodSubset(self, data, step):
        dataLength = len(data)
        index = 0
        while index < dataLength:

            if sum(data[index:index+step])>0:
                return data[index:index+step]
            index += step

        return data[0:step]
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

    def push(self, date, consumption, coal, gas, hidroelectric, nuclear, wind, solar, biomass, production):
        self.date.append(date)
        self.consumption.append(consumption)
        self.coal.append(coal)
        self.gas.append(gas) 
        self.hidroelectric.append(hidroelectric)
        self.nuclear.append(nuclear)
        self.wind.append(wind)
        self.solar.append(solar)
        self.biomass.append(biomass)
        self.production.append(production)

    def getArrayForKeys(self):
        return self.__dict__

class Stats_Object:
    def __init__(self):
        self.sum = []
        self.avg = []

class Statistics(Resource):
    def readCachedStatistics(self):
        cacheFile = open(Utils.stats_cache_path, "r")
        cachedContent = cacheFile.read()
        return cachedContent

    def writeStatisticsCache(self, cachedContent):
        cacheFile = open(Utils.stats_cache_path, "w")
        cacheFile.write(cachedContent)

    def deleteCachedStatistics(self):
        cacheFile = open(Utils.stats_cache_path, "w")
        cacheFile.write('')
        

    def get(self):


        x = self.readCachedStatistics()
        if x != '':
            return json.loads(x)

        csv_file = open(Utils.train_file_path, "r")
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        data = Model_Statistics()
        for row in csv_reader:
            if first == True:
                first = False
                continue 
            data.push(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

        stats = Stats_Object()
        response = jsonify(self.buildDictionaryStats(stats, data))
        self.writeStatisticsCache(response.get_data(as_text=True))
        return response

    def buildDictionaryStats(self, stats, data):
        dataDict = data.getArrayForKeys()
        for key in dataDict.keys():
            resultsDictionary = dict()
            resultsDictionary['sum'] = sum([float(i) for i in dataDict[key]])
            resultsDictionary['avg'] = numpy.mean([float(i) for i in dataDict[key]])
            resultsDictionary['data'] = dataDict[key][0:1000]
            dataDict[key] = resultsDictionary
        
        return dataDict

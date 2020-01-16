from flask_restful import Resource
from flask import jsonify
import json
import utils as Utils
import os
import csv
from config import trained_models_dir_path
from statistics import Statistics, Model_Statistics

class Monthly_Statistics(Resource):
    def get(self):
        statistics = Statistics(Utils.monthly_stats_cache_path)
        
        x = statistics.readCachedStatistics()
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

        response = jsonify(statistics.extractMonthlyData(data))
        statistics.writeStatisticsCache(response.get_data(as_text=True))
        return response

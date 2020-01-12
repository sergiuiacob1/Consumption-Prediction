from flask_restful import Resource
import json
import utils as Utils
import os
from config import trained_models_dir_path


class Statistics(Resource):
    def get(self):
        x =  '{ "name":"John", "pula":"incur", "macacu":"pestetot"}'
        response = json.loads(x)
        return response

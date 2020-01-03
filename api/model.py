from flask_restful import Resource
import json
import utils as Utils
import os
from config import trained_models_dir_path


class Model(Resource):
    def get(self):
        models = [x for x in os.listdir(os.path.join(
            os.getcwd(), trained_models_dir_path)) if x.endswith('.json')]
        data = []
        for model in models:
            with open(os.path.join(os.getcwd(), trained_models_dir_path, model), 'r') as f:
                model_data = json.load(f)
            obj = {
                "model_name": model.split('.json')[0],
                "configuration": model_data
            }
            data.append(obj)
        response = Utils.build_json_response(data)
        return response

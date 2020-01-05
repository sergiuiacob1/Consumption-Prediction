from flask_restful import Resource, request
import pandas as pd
import math
import joblib
import os
import json
import utils as Utils
from config import trained_models_dir_path
from data_processing import process_data


class Prediction(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            data = json.dumps(data)
            X = pd.read_json(data)
            # drop rows that are all null
            X.dropna(how='all', inplace=True)
            if self.data_is_valid(X):
                # TODO data has to be processed here
                # temporarily dropping the Date column
                X = process_data(X)
                print(f'Predicting \n{X}')
                predictions = self.get_prediction(X.values)
                if predictions is None:
                    response = Utils.build_json_response(
                        "Could not get predictions. No models trained, perhaps?", success=False, status_code=501)
                else:
                    response = Utils.build_json_response(predictions)
                print('Predicting done')
            else:
                print(f'Data is invalid')
                response = Utils.build_json_response(
                    "Data is malformed", success=False, status_code=422)
        except Exception as e:
            print(f'Something failed: {str(e)}')
            response = Utils.build_json_response(
                str(e), success=False, status_code=400)

        return response

    def data_is_valid(self, df):
        """`df` is a `pandas.DataFrame` object. Makes sure there are no NaN's in the DataFrame"""
        if df.isnull().values.any() or len(df) == 0:
            return False
        return True

    def get_prediction(self, X):
        model = self.get_best_model()
        if model is None:
            return None
        print(f'Predicting with {model}')
        return model.predict(X)

    def get_best_model(self):
        # Check that the directory with models exists
        if os.path.exists(trained_models_dir_path) is False:
            return None
        # Get the best model based on its mse_score (Mean Squared Error Score)
        path = os.path.join(os.getcwd(), trained_models_dir_path)
        models_info = [x for x in os.listdir(path) if x.endswith(".json")]
        if len(models_info) == 0:
            return None

        min_score = math.inf
        for x in models_info:
            model_info_path = os.path.join(path, x)
            with open(model_info_path, 'r') as f:
                data = json.load(f)
            if data['mse_score'][-1] < min_score:
                min_score = data['mse_score']
                best_model_name = x.split('.json')[0] + '.pkl'

        try:
            model = joblib.load(os.path.join(path, best_model_name))
            print(f'Model chosen was {best_model_name}')
        except Exception as e:
            print(f'Could not load model {best_model_name}')

        return model

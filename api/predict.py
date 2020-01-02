from flask_restful import Resource, reqparse
import pandas as pd
import joblib
import os
import numpy as np
import utils as Utils
import json
import utils as Utils


class Prediction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        for column in Utils.X_original_columns:
            data_type = float
            if column == 'Date':
                data_type = int
            self.parser.add_argument(column, type=data_type, action='append')

    def post(self):
        data = self.parser.parse_args()
        X = pd.read_json(json.dumps(data))
        if self.data_is_valid(X):
            # TODO data has to be processed here
            # temporarily dropping the Date column
            X.drop(columns='Date', inplace=True)
            predictions = self.get_prediction(X.values)
            print(f'Prediction for {X} is {predictions}')
            response = Utils.build_json_response(predictions)
        else:
            response = Utils.build_json_response(
                "Data is malformed", success=False, status_code=422)

        return response

    def data_is_valid(self, df):
        """`X` is a `pandas.DataFrame` object. Makes sure there are no NaN's in the DataFrame"""
        if df.isnull().values.any():
            return False
        return True

    def get_prediction(self, X):
        model = self.get_best_model()
        return model.predict(X)

    def get_best_model(self):
        file_path = os.path.join(os.getcwd(), 'trained_models', 'model_2.pkl')
        model = joblib.load(file_path)
        return model

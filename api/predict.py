from flask_restful import Resource, reqparse
import joblib
import os
import numpy as np
import utils as Utils
import json
import utils as Utils


class Prediction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        for column in Utils.X_columns:
            self.parser.add_argument(column, type=float)

    def get(self):
        kwargs = self.parser.parse_args()
        X = np.array(list(kwargs.values()))
        X = X.reshape(1, -1)
        prediction = self.get_prediction(X)
        print(f'Prediction for {X} is {prediction}')
        data = {'success': True, 'prediction': prediction}
        return Utils.build_json_response(data, 200)

    def get_prediction(self, X):
        file_path = os.path.join(os.getcwd(), 'trained_models', 'model.pkl')
        model = joblib.load(file_path)
        return model.predict(X)

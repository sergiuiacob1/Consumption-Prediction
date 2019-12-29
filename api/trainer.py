from flask_restful import Resource, reqparse
from flask import json
import threading
import pandas as pd
from sklearn.neural_network import MLPClassifier
import joblib
import os
import utils as Utils
from data_processing import get_data
from config import trained_models_dir_path

no_of_running_threads_lock = threading.Lock()
no_of_running_threads = 0

class Trainer(Resource):
    allowed_train_parameters = {
        "learning_rate": float,
        "max_iter": int,
    }

    def __init__(self):
        self.parser = reqparse.RequestParser()
        for x in Trainer.allowed_train_parameters:
            self.parser.add_argument(
                x, type=Trainer.allowed_train_parameters[x])

    def post(self):
        kwargs = self.parser.parse_args()
        t = threading.Thread(target=self.train, kwargs=kwargs)
        t.start()
        response = Utils.build_json_response(
            f'Training model with: {kwargs}')
        return response

    def train(self, **train_parameters):
        print(f'Training new model with eta: {train_parameters}')
        print('Loading data...')
        data = get_data()

        model = MLPClassifier(hidden_layer_sizes=(
            36), **train_parameters, verbose=True)
        X = data[Utils.X_columns][:10000]
        y = data[Utils.y_column][:10000]

        print('Training model...')
        try:
            model.fit(X, y)
        except Exception as e:
            print(
                f'Could not train model with {train_parameters}.\nError: {e}')
        else:
            # if training the model succedeed
            self.save_trained_model(model)
            print('Training done')

    def save_trained_model(self, model):
        print('Saving model...')
        model_name = self.get_next_model_name()
        file_path = os.path.join(
            os.getcwd(), trained_models_dir_path, model_name)
        joblib.dump(model, file_path)
        print(f'Model saved as {model_name}')

    def get_next_model_name(self):
        # TODO
        # vad care e ultimul model
        absolute_trained_models_dir_path = os.path.abspath(
            os.path.join(os.getcwd(), trained_models_dir_path))
        no_of_existing_models = len(
            os.listdir(absolute_trained_models_dir_path))

        # mai am si thread-uri care ruleaza in fundal
        # daca ultimul model e model_10 si am 2 threaduri care ruleaza
        # atunci de fapt ultimul model ar fi model_12, deci urmatorul va fi model_13
        return f'model_{no_of_existing_models + no_of_running_threads + 1}.pkl'


if __name__ == '__main__':
    trainer = Trainer()
    trainer.train()

from flask_restful import Resource, reqparse
from flask import json
import threading
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import joblib
import os
import utils as Utils
from data_processing import get_train_data, get_test_data
from config import trained_models_dir_path


def get_last_model_number():
    path = os.path.join(os.getcwd(), trained_models_dir_path)
    files = os.listdir(path)
    if len(files) == 0:
        return 1
    files = [x for x in files if x.endswith('.pkl')]
    numbers = [int(x.split('_')[1].split('.pkl')[0]) for x in files]
    return max(numbers)


last_model_number = get_last_model_number()
last_model_number_lock = threading.Lock()


class Trainer(Resource):
    allowed_train_parameters = {
        "learning_rate": str,
        "learning_rate_init": float,
        "max_iter": int,
        "tol": float,
        "hidden_layer_sizes": int,
        "activation": str,
        "solver": str,
        "batch_size": int,
        "warm_start": bool,
    }

    def __init__(self):
        self.parser = reqparse.RequestParser()
        for x in Trainer.allowed_train_parameters:
            if x is 'hidden_layer_sizes':
                action = 'append'
            else:
                action = None
            self.parser.add_argument(
                x, type=Trainer.allowed_train_parameters[x], action=action)

    def post(self):
        kwargs = self.parser.parse_args()
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        t = threading.Thread(target=self.train, kwargs=kwargs)
        t.start()
        response = Utils.build_json_response(
            f'Training model with: {kwargs}')
        return response

    def train(self, **train_parameters):
        print(f'Training new model with eta: {train_parameters}')
        print('Loading data...')
        data = get_train_data()

        model = MLPRegressor(**train_parameters, verbose=True)
        X_train, X_test, y_train, y_test = train_test_split(
            data[Utils.X_columns], data[Utils.y_column], test_size=0.10, random_state=42)

        print('Training model...')
        try:
            model.fit(X_train, y_train)
        except Exception as e:
            print(
                f'Could not train model with {train_parameters}.\nError: {e}')
        else:
            # if training the model succedeed
            score = self.evaluate_model(model, X_test, y_test)
            print(f'Model score: {score}')
            self.save_trained_model(model, train_parameters, score)
            print('Training done')

    def evaluate_model(self, model, X, y):
        """Returns the Mean Squared Error for the test data"""
        y_pred = model.predict(X)
        score = mean_squared_error(y, y_pred)
        return score

    def save_trained_model(self, model, train_parameters, score):
        print('Saving model...')
        print(model)
        model_name = self.get_next_model_name()
        file_path = os.path.join(
            os.getcwd(), trained_models_dir_path, model_name)

        try:
            t = threading.Thread(
                target=self.save_model_configuration, args=(file_path, train_parameters, score))
            t.start()
            t.join()
        except Exception as e:
            print(f'Failed to save model {model_name}: {e}')
        else:
            joblib.dump(model, file_path)
            print(f'Model saved as {model_name}')

    def save_model_configuration(self, file_path, train_parameters, score):
        # save the configuration in the same folder with the same name, but in a json file
        file_path = file_path.split('.pkl')[0] + '.json'
        config = {
            "train_parameters": train_parameters,
            "mse_score": score,
        }
        with open(file_path, 'w') as f:
            json.dump(config, f)

    def get_next_model_name(self):
        global last_model_number, last_model_number_lock
        last_model_number_lock.acquire()

        last_model_number += 1
        model_name = f'model_{last_model_number}.pkl'

        last_model_number_lock.release()
        return model_name


if __name__ == '__main__':
    trainer = Trainer()
    trainer.train()

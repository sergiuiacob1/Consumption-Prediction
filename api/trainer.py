from flask_restful import Resource, request
from flask import json
import threading
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import joblib
import os
import utils as Utils
from data_processing import get_train_data
from config import trained_models_dir_path

# TODO
# import lightgbm as lgb
import xgboost as xgb


def get_last_model_number():
    path = os.path.join(os.getcwd(), trained_models_dir_path)
    files = os.listdir(path)
    if len(files) == 0:
        return 1
    files = [x for x in files if x.endswith('.pkl')]
    numbers = [int(x.split('_')[1].split('.pkl')[0]) for x in files]
    if len(numbers) == 0:
        return 1
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

    def post(self):
        train_parameters = request.get_json(force=True)
        train_parameters = self.filter_train_parameters(train_parameters)
        t = threading.Thread(target=self.train, kwargs=train_parameters)
        t.start()
        response = Utils.build_json_response(
            f'Training model with: {train_parameters}')
        return response

    def filter_train_parameters(self, train_parameters):
        train_parameters = {k: v for k, v in train_parameters.items()
                            if k in Trainer.allowed_train_parameters and type(v) == Trainer.allowed_train_parameters[k]}
        return train_parameters

    def train(self, **train_parameters):
        print(f'Training new model with: {train_parameters}')
        print('Loading data...')
        data = get_train_data()

        model = MLPRegressor(**train_parameters, verbose=True)
        # This data object may contain additional columns to Utils.X_original_columns
        X_columns = list(data.columns)
        y_column = Utils.y_column
        X_columns.remove(y_column)
        X_train, X_test, y_train, y_test = train_test_split(
            data[X_columns], data[y_column], test_size=0.10)

        xg_trn_data = xgb.DMatrix(X_train, y_train)
        xg_vld_data = xgb.DMatrix(X_test, y_test)
        num_round = 50  # value used only for commiting the kernel fast
        xgb_param = {"objective": "reg:squarederror" if xgb.__version__ > '0.82' else 'reg:linear',
                     'eta': 0.1, 'booster': 'gbtree', 'max_depth': 8, 'min_child_weight': 10, 'gamma': 5, 'subsample': 0.75,
                     'colsample_bytree': 1, 'lambda': 10}
        watchlist = [(xg_trn_data, "train"), (xg_vld_data, "valid")]
        bst = xgb.train(xgb_param, xg_trn_data, num_round, watchlist)

        # params = {
        #     'boosting_type': 'gbdt',
        #     'objective': 'root_mean_squared_error',
        #     'metric': 'l2_root',
        #     'num_leaves': 31,
        #     'learning_rate': 0.05,
        #     'feature_fraction': 0.9,
        #     'bagging_fraction': 0.8,
        #     'bagging_freq': 5,
        #     'verbose': 0
        # }

        # lgb_train_data = lgb.Dataset(X_train, y_train)
        # lgb_valid_data = lgb.Dataset(X_test, y_test)
        # gbm = lgb.train(params,
        #                 lgb_train_data,
        #                 num_boost_round=300,  # initial value used 60000
        #                 valid_sets=lgb_valid_data,
        #                 early_stopping_rounds=5)

        # return

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

from flask_restful import Resource, request
from flask import json
import threading
import joblib
import time
import os
import utils as Utils
from data_processing import get_train_data
from config import trained_models_dir_path
import ast

import xgboost as xgb

from keras.models import Sequential
from keras.layers import Dense, Dropout, ReLU
from keras import optimizers, regularizers, initializers


def get_last_model_number():
    path = os.path.join(os.getcwd(), trained_models_dir_path)
    os.makedirs(path, exist_ok=True)
    files = os.listdir(path)
    if len(files) == 0:
        return 0
    files = [x for x in files if x.endswith('.pkl')]
    numbers = [int(x.split('_')[1].split('.pkl')[0]) for x in files]
    if len(numbers) == 0:
        return 0
    return max(numbers)


last_model_number = get_last_model_number()
last_model_number_lock = threading.Lock()


class Trainer(Resource):
    # (type, default_value)
    allowed_train_parameters = {
        "optimizer": (str, "adam"),
        "learning_rate": (float, 0.01),
        "learning_rate_decay": (float, 0.0000001),
        "epochs": (int, 500),
        "hidden_layer_sizes": (list, 100),
        "layer_activations": (list, "relu"),
        "layer_dropout_values": (list, 0.0),
        "weight_initializers": (list, "glorot_uniform"),
        "batch_size": (int, 16),
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
        # By default, 2 hidden layers
        if "hidden_layer_sizes" not in train_parameters:
            train_parameters["hidden_layer_sizes"] = [100, 32]
        no_layers = len(train_parameters["hidden_layer_sizes"])

        for k in Trainer.allowed_train_parameters:
            if Trainer.allowed_train_parameters[k][0] is not list:
                # the type isn't list
                if k not in train_parameters:
                    # set the default value
                    train_parameters[k] = Trainer.allowed_train_parameters[k][1]
                else:
                    # convert to the type I need
                    train_parameters[k] = Trainer.allowed_train_parameters[k][0](
                        train_parameters[k])
            else:
                # this is a list
                if k not in train_parameters:
                    # default value
                    train_parameters[k] = [
                        Trainer.allowed_train_parameters[k][1]] * no_layers
                else:
                    # make sure all lists have the same length
                    remainder = no_layers - len(train_parameters[k])
                    if remainder < 0:
                        train_parameters[k] = train_parameters[k][:no_layers]
                    else:
                        train_parameters[k] = train_parameters[k] + \
                            [Trainer.allowed_train_parameters[k][1]] * remainder

        # convert these to ints
        for k in ["hidden_layer_sizes", "layer_dropout_values"]:
            train_parameters[k] = list(
                map(lambda x: ast.literal_eval(str(x)), train_parameters[k]))

        return train_parameters

    def train(self, **train_parameters):
        print(f'Training new model with: {train_parameters}')
        print('Loading data...')
        start_time = time.time()
        data = get_train_data()
        data.drop([85008, 85009, 146999, 159698, 161540, 161541], inplace=True)
        # shuffle the data
        data = data.sample(frac=1).reset_index(drop=True)

        # Keras version below
        # This data object may contain additional columns to Utils.X_original_columns
        X_columns = list(data.columns)
        y_column = Utils.y_column
        X_columns.remove(y_column)

        model = Sequential()
        initializer = 'glorot_normal'
        my_optimizers = {
            "sgd": optimizers.SGD(lr=train_parameters["learning_rate"], decay=train_parameters["learning_rate_decay"], momentum=0.9, nesterov=True),
            "adagrad": optimizers.Adagrad(lr=train_parameters["learning_rate"], decay=train_parameters["learning_rate_decay"]),
            "adam": optimizers.Adam(lr=train_parameters["learning_rate"], decay=train_parameters["learning_rate_decay"]),
            "rmsprop": optimizers.RMSprop(lr=train_parameters["learning_rate"], decay=train_parameters["learning_rate_decay"]),
        }

        model = Sequential()
        for i in range(0, len(train_parameters["hidden_layer_sizes"])):
            no_neurons = train_parameters["hidden_layer_sizes"][i]
            activation = train_parameters["layer_activations"][i]
            dropout_value = train_parameters["layer_dropout_values"][i]
            weight_initializer = train_parameters["weight_initializers"][i]
            if i == 0:
                input_shape = (len(X_columns), )
            else:
                input_shape = (train_parameters["hidden_layer_sizes"][i-1], )
            model.add(Dense(no_neurons, activation=activation,
                            input_shape=input_shape, kernel_initializer=weight_initializer))
            model.add(Dropout(dropout_value))
        # the value we're going to predict
        model.add(Dense(1, activation="linear"))

        print('Training model...')
        try:
            model.compile(loss='mean_squared_error',
                          optimizer=my_optimizers[train_parameters["optimizer"]])
            fit_history = model.fit(data[X_columns].values, data[y_column].values, validation_split=0.1,
                                    batch_size=train_parameters["batch_size"], epochs=train_parameters["epochs"], workers=4)
        except Exception as e:
            print(
                f'Could not train model with {train_parameters}.\nError: {e}')
        else:
            # if training the model succedeed
            score = fit_history.history['val_loss']
            print(f'Model score: {score}')
            self.save_trained_model(
                model, train_parameters, score, time.time() - start_time)
            print(f'Training took {time.time() - start_time} seconds')

        # xg_trn_data = xgb.DMatrix(X_train, y_train)
        # xg_vld_data = xgb.DMatrix(X_test, y_test)
        # num_round = 50  # value used only for commiting the kernel fast
        # xgb_param = {"objective": "reg:squarederror" if xgb.__version__ > '0.82' else 'reg:linear',
        #              'eta': 0.1, 'booster': 'gbtree', 'max_depth': 8, 'min_child_weight': 10, 'gamma': 5, 'subsample': 0.75,
        #              'colsample_bytree': 1, 'lambda': 10}
        # watchlist = [(xg_trn_data, "train"), (xg_vld_data, "valid")]
        # bst = xgb.train(xgb_param, xg_trn_data, num_round, watchlist)
        # return

    def save_trained_model(self, model, train_parameters, score, training_time):
        print('Saving model...')
        print(model)
        model_name = self.get_next_model_name()
        file_path = os.path.join(
            os.getcwd(), trained_models_dir_path, model_name)

        try:
            t = threading.Thread(
                target=self.save_model_configuration, args=(file_path, train_parameters, score, training_time))
            t.start()
            t.join()
        except Exception as e:
            print(f'Failed to save model {model_name}: {e}')
        else:
            joblib.dump(model, file_path)
            print(f'Model saved as {model_name}')

    def save_model_configuration(self, file_path, train_parameters, score, training_time):
        # save the configuration in the same folder with the same name, but in a json file
        file_path = file_path.split('.pkl')[0] + '.json'
        config = {
            "train_parameters": train_parameters,
            "mse_score": score,
            "training_time": training_time
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

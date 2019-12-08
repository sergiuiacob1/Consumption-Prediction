from flask_restful import Resource, reqparse
import threading
import pandas as pd
from sklearn.neural_network import MLPClassifier
import joblib
import os
import utils as Utils


class Trainer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('learning_rate', type=float)
        self.parser.add_argument('epochs', type=int)

    def post(self):
        kwargs = self.parser.parse_args()
        t = threading.Thread(target=self.train, kwargs=kwargs)
        t.start()
        return {'Training model with: ': str(kwargs)}

    def train(self, learning_rate=0.5, **kwargs):
        print(f'Training new model with eta: {kwargs}')
        print('Loading data...')
        data = pd.read_csv('./../data/train_electricity.csv')

        model = MLPClassifier(hidden_layer_sizes=(36), max_iter=5)
        X = data[Utils.X_columns]
        y = data[Utils.y_column]
        print('Training model...')
        model.fit(X, y)
        self.save_trained_model(model)
        print('Training done')

    def save_trained_model(self, model):
        print('Saving model...')
        file_path = os.path.join(os.getcwd(), 'trained_models', 'model.pkl')
        joblib.dump(model, file_path)


if __name__ == '__main__':
    trainer = Trainer()
    trainer.train()

from http.server import HTTPServer
from flask import Flask, request
from flask_restful import Api

from model import Model
from trainer import Trainer
from predict import Prediction


class Server:
    port = 3001

    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.api.add_resource(Model, '/models')
        self.api.add_resource(Trainer, '/train')
        self.api.add_resource(Prediction, '/predict')

    def run(self):
        self.app.run(port=Server.port)

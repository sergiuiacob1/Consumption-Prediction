from http.server import HTTPServer
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
import simplejson
import numpy as np

from model import Model
from trainer import Trainer
from predict import Prediction


class CustomJSONEncoder(simplejson.JSONEncoder):
    """Used to help jsonify numpy arrays or lists that contain numpy data types."""

    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return simplejson.JSONEncoder.default(self, obj)


class Server:
    port = 3001

    def __init__(self):
        self.app = Flask(__name__)
        cors = CORS(self.app)
        self.app.config['CORS_HEADERS'] = 'Content-Type'
        # the instruction below defines how the flask responses will be encoded
        # necessary because numpy arrays aren't directly JSON serializable
        self.app.json_encoder = CustomJSONEncoder
        self.api = Api(self.app)

        self.api.add_resource(Model, '/models')
        self.api.add_resource(Trainer, '/train')
        self.api.add_resource(Prediction, '/predict')

    def run(self):
        # TODO change when ready for deployment
        self.app.run(port=Server.port, debug=True)

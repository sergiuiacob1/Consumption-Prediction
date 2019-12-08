from flask_restful import Resource, reqparse


class Trainer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('learning_rate', type=str)
        self.parser.add_argument('epochs', type=str)

    def post(self):
        args = self.parser.parse_args()
        return {'I have received:': str(args)}

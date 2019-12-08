from flask_restful import Resource


class Model(Resource):
    def get(self):
        return {'model': 'lorem ipsum'}

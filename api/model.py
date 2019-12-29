from flask_restful import Resource
import json
import utils as Utils


class Model(Resource):
    def get(self):
        data = {'success': True,
                'message': 'Information about models will be here',
                'models': []}
        response = Utils.build_json_response(data, 200)
        return response

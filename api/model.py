from flask_restful import Resource


class Model(Resource):
    def get(self):
        response = {'success': True,
                    'message': f'The models will be here'}
        return json.dumps(response)

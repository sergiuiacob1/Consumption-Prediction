from flask import jsonify

X_columns = ['Coal_MW', 'Gas_MW',	'Hidroelectric_MW', 'Nuclear_MW',
             'Wind_MW', 'Solar_MW', 'Biomass_MW', 'Production_MW']
y_column = 'Consumption_MW'


def build_json_response(data, success=True, status_code=200):
    """Makes a Flask response with a JSON encoded body"""
    response = {
        "success": success,
        "data": data,
    }
    response = jsonify(response)
    response.status_code = status_code
    return response

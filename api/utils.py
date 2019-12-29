from flask import make_response
import json

X_columns = ['Coal_MW', 'Gas_MW',	'Hidroelectric_MW', 'Nuclear_MW',
             'Wind_MW', 'Solar_MW', 'Biomass_MW', 'Production_MW']

y_column = 'Consumption_MW'


def build_json_response(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    resp.mimetype = "application/json"
    return resp

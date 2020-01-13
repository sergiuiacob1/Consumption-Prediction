from flask import jsonify

X_original_columns = ['Date', 'Coal_MW', 'Gas_MW',	'Hidroelectric_MW',
                      'Nuclear_MW', 'Wind_MW', 'Solar_MW', 'Biomass_MW', 'Production_MW']
y_column = 'Consumption_MW'

train_file_path = '../data/train_electricity.csv'

monthly_stats_cache_path = 'api_cache/monthly_stats_cache'

general_stats_cache_path = 'api_cache/general_stats_cache'


def build_json_response(data, success=True, status_code=200):
    """Makes a Flask response with a JSON encoded body"""
    response = {
        "success": success,
        "data": data,
    }
    response = jsonify(response)
    response.status_code = status_code
    return response

`main.py` will start a Python server that treats `GET` and `POST` requests

# Models
## GET request
Fetching at `api/models` will return a json with information about the existing trained models.

# Training
Coming soon...

# Prediction
## POST request
Example of POST at `api/prediction`
```
{
  "Date": [100, 200, 300],
  "Coal_MW": [100, 200, 300],
  "Gas_MW": [100, 200, 300],
  "Hidroelectric_MW": [100, 200, 300],
  "Nuclear_MW": [100, 200, 300],
  "Wind_MW": [100, 200, 300],
  "Solar_MW": [100, 200, 300],
  "Biomass_MW": [100, 200, 300],
  "Production_MW": [100, 200, 300],
}
```
All lists must have the same length. The api route will provide a list of predictions for the data, e.g. `[312.5, 400.7, 512]`

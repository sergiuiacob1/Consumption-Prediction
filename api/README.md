`main.py` will start a Python server that treats `GET` and `POST` requests

# Models
## GET request
Fetching at `api/models` will return a json with information about the existing trained models.

# Training
Coming soon...

# Predict
## POST request
Example of POST at `api/predict`
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
All lists must have the same length. The api route will return a json of type:
```
{
  "success": True,
  "data": [312.5, 400.7, 512]
 }
```

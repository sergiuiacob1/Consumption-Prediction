import pandas as pd
import config
from sklearn import preprocessing

def get_data():
    returnData = []
    inputData = pd.read_csv(config.train_data_path)
    inputData.drop(axis=1, columns="Date", inplace=True)
    min_max_scaler = preprocessing.MinMaxScaler()
    transformedData = min_max_scaler.fit_transform(inputData)
    returnData = pd.DataFrame(data=transformedData, columns=inputData.columns)
    return returnData

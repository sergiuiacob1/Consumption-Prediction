import pandas as pd
import config
from sklearn import preprocessing

def process_data(file_path):
    returnData = []
    if file_path is not None:
        inputData = pd.read_csv(file_path)
        inputData.drop(axis=1, columns="Date", inplace=True)
        min_max_scaler = preprocessing.MinMaxScaler()
        transformedData = min_max_scaler.fit_transform(inputData)
        returnData = pd.DataFrame(data=transformedData, columns=inputData.columns)
    return returnData

def get_test_data():
    returnData = []
    if config.test_data_path is not None:
        returnData = process_data(config.test_data_path)
    return returnData

def get_train_data():
    returnData = []
    if config.train_data_path is not None:
        returnData = process_data(config.train_data_path)
    return returnData
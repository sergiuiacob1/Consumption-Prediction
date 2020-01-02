import pandas as pd
import config
from sklearn import preprocessing
from utils import X_original_columns as x_columns

x_columns = list(x_columns)
x_columns.remove('Date')

def process_data(dataframe):
    new_features_input = add_new_features(dataframe)
    new_features_input.drop(axis=1, columns="Date", inplace=True)
    min_max_scaler = preprocessing.MinMaxScaler()
    new_features_input[x_columns] = min_max_scaler.fit_transform(new_features_input[x_columns])
    return new_features_input

def get_train_data():
    return pd.read_csv(config.processed_train_data)

def add_new_features(dataframe):
    new_features = ["Year", "Month", "Week", "Day", "Dayofyear", "Dayofweek", "Hour"]
    one_hot_features = ["Month", "Day", "Week", "Dayofweek", "Hour"]
    datetime = pd.to_datetime(dataframe.Date, unit="s")
    for feature in new_features:
        new_feature = getattr(datetime.dt, feature.lower())
        if feature in one_hot_features:
            dataframe = pd.concat([dataframe, pd.get_dummies(new_feature, prefix=feature)], axis=1)
        else:
            dataframe[feature] = new_feature
    return dataframe

def process_training_data():
    input_data = pd.read_csv(config.train_data_path)
    new_features_input_data = process_data(input_data)

    return new_features_input_data
    

if __name__ == '__main__':
    # process training data
    df = process_training_data()
    df.to_csv(config.processed_train_data, index=False)
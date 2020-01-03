import pandas as pd
import config
from sklearn import preprocessing
from utils import X_original_columns as x_columns
import joblib
import os

x_columns = list(x_columns)
x_columns.remove('Date')

one_hot_features = ["Month", "Day", "Week", "Dayofweek", "Hour"]


def process_data(dataframe, rebuild=False):
    print('Processing data...')
    dataframe = add_new_features(dataframe, rebuild)
    dataframe.drop(axis=1, columns="Date", inplace=True)
    apply_scaling(dataframe, rebuild)
    return dataframe


def apply_scaling(df, rebuild):
    print('Applying MinMaxScaler...')
    if rebuild is True:
        min_max_scaler = build_normalizer(df[x_columns])
    else:
        min_max_scaler = joblib.load(config.normalizer_path)
    df[x_columns] = min_max_scaler.transform(df[x_columns])


def build_normalizer(df_to_scale):
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_scaler.fit(df_to_scale)
    # make sure the directory in which the one_hot_encoder will be saved exists
    os.makedirs(os.path.dirname(config.normalizer_path), exist_ok=True)
    joblib.dump(min_max_scaler, config.normalizer_path)
    return min_max_scaler


def get_train_data():
    return pd.read_csv(config.processed_train_data)


def add_new_features(dataframe, rebuild=False):
    global one_hot_features
    new_features = ["Year", "Month", "Week",
                    "Day", "Dayofyear", "Dayofweek", "Hour"]
    datetime = pd.to_datetime(dataframe.Date, unit="s")

    for feature in new_features:
        new_feature = getattr(datetime.dt, feature.lower())
        dataframe[feature] = new_feature

    if rebuild is True:
        one_hot_encoder = build_one_hot_encoder(dataframe)
    else:
        one_hot_encoder = joblib.load(config.one_hot_encoder_path)

    # apply the one hot encoding transformation
    print('Applying one hot encoding')
    one_hot_dataframe = pd.DataFrame(data=one_hot_encoder.transform(
        dataframe[one_hot_features]).toarray(), columns=one_hot_encoder.get_feature_names(one_hot_features))
    dataframe = pd.concat([dataframe, one_hot_dataframe], axis=1)
    dataframe.drop(columns=one_hot_features, inplace=True)

    return dataframe


def process_training_data():
    print('Loading data...')
    original_train_data = pd.read_csv(config.train_data_path)
    proceesed_data = process_data(original_train_data, rebuild=True)
    return proceesed_data


def build_one_hot_encoder(df):
    global one_hot_features
    print('Building one hot encoder')
    one_hot_encoder = preprocessing.OneHotEncoder()
    one_hot_encoder.fit(df[one_hot_features])
    # serialize the oneHotEncoder
    # make sure the directory in which the one_hot_encoder will be saved exists
    os.makedirs(os.path.dirname(
        config.one_hot_encoder_path), exist_ok=True)
    joblib.dump(one_hot_encoder, config.one_hot_encoder_path)
    print('One hot encoder built')
    return one_hot_encoder


if __name__ == '__main__':
    # process training data
    df = process_training_data()
    print('Saving processed data...')
    df.to_csv(config.processed_train_data, index=False)

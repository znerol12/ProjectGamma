import pandas as pd


def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['Upper Band'] = data['SMA'] + num_std_dev * data['Close'].rolling(
        window=window).std()
    data['Lower Band'] = data['SMA'] - num_std_dev * data['Close'].rolling(
        window=window).std()
    return data

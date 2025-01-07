import pandas as pd
import numpy as np

def ema_crossover_strategy(data, ticker, short_window=1, long_window=3):
    data['short_ema'] = data[f'Close_{ticker}'].ewm(span=short_window, adjust=False).mean()
    data['long_ema'] = data[f'Close_{ticker}'].ewm(span=long_window, adjust=False).mean()

    data['signal'] = 0
    data.loc[data['short_ema'] > data['long_ema'], 'signal'] = 1  # Buy
    data.loc[data['short_ema'] <= data['long_ema'], 'signal'] = -1  # Sell

    return data.index[data['signal'].diff() != 0]



def bollinger_bands_strategy(data, ticker, window=20):
    data['sma'] = data[f'Close_{ticker}'].rolling(window=window, min_periods=1).mean()
    data['std_dev'] = data[f'Close_{ticker}'].rolling(window=window, min_periods=1).std()

    data['upper_band'] = data['sma'] + (2 * data['std_dev'])
    data['lower_band'] = data['sma'] - (2 * data['std_dev'])

    data['signal'] = 0
    data.loc[data[f'Close_{ticker}'] > data['upper_band'], 'signal'] = -1  # Sell
    data.loc[data[f'Close_{ticker}'] < data['lower_band'], 'signal'] = 1  # Buy

    return data.index[data['signal'].diff() != 0]




def moving_average_volume_strategy(data, ticker, price_window=10, volume_window=20):
    data['price_ma'] = data[f'Close_{ticker}'].rolling(price_window).mean()
    data['volume_ma'] = data[f'Volume_{ticker}'].rolling(volume_window).mean()

    data['signal'] = 0
    data.loc[(data[f'Close_{ticker}'] > data['price_ma']) & (data[f'Volume_{ticker}'] > data['volume_ma']), 'signal'] = 1  # Buy
    data.loc[(data[f'Close_{ticker}'] <= data['price_ma']) | (data[f'Volume_{ticker}'] <= data['volume_ma']), 'signal'] = -1  # Sell

    return data.index[data['signal'].diff() != 0]


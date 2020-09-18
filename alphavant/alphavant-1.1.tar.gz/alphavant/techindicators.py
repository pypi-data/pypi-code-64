import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas as pd
import zipfile
import json
import tensorflow as tf
from time_series import transpose_dataframe


def get_response_as_df(response, indicator):
    response = response.json()
    response = response[f'Technical Analysis: {indicator}']
    df = pd.DataFrame.from_dict(response)
    indicator_df = transpose_dataframe(df)
    indicator_df = pd.DataFrame(indicator_df, columns=([list(df.index)]))
    # other_columns = ['Value' for i in range(indicator_df.shape[1]-1)]
    # indicator_df = pd.DataFrame(indicator_df, columns = ([f'{indicator}'] + other_columns))
    return indicator_df


def get_technical_indicator(ticker, api_key, time_interval='daily', window_size=15, series_type='close', indicator='EMA'):
    indicator_df = 0
    base_url = 'https://www.alphavantage.co/query?'
    if indicator == 'SMA':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'RSI':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'EMA':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'WMA':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'DEMA':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'TEMA':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'TRIMA':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'KAMA':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'VWAP':
        default_time_interval = '15min'
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={default_time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MAMA':
        fast_limit = 0.01
        slow_limit = 0.01
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&fast_limit={fast_limit}&slow_limit{slow_limit}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'T3':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MACD':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MACDEXT':
        fast_limit = 0.01
        slow_limit = 0.01
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&fast_limit={fast_limit}&slow_limit{slow_limit}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'STOCH':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'STOCHF':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'STOCHRSI':
        # function=STOCHRSI&symbol=IBM&interval=daily&time_period=10&series_type=close&fastkperiod=6&fastdmatype=1&apikey=demo
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&fastkperiod=6&fastdmatype=1&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'WILLR':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'ADX':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'ADXR':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'APO':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&series_type={series_type}&fast_period=10&matype=1&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'PPO':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&series_type={series_type}&fast_period=10&matype=1&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MOM':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'BOP':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'CCI':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'CMO':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'ROC':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'ROCR':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'AROON':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'AROONOSC':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MFI':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'TRIX':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'ULTOSC':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&timeperiod1=8&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'DX':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MINUS_DI':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'PLUS_DI':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MINUS_DM':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'PLUS_DM':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'BBANDS':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&nbdevup=3&nbdevdn=3&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MIDPOINT':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'MIDPRICE':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'SAR':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&acceleration=0.05&maximum=0.25&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'TRANGE':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'ATR':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'NATR':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&time_period={window_size}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'AD':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&apikey={api_key}')
        response = response.json()
        response = response[f'Technical Analysis: Chaikin A/D']
        df = pd.DataFrame.from_dict(response)
        indicator_df = transpose_dataframe(df)
        indicator_df = pd.DataFrame(indicator_df, columns=([list(df.index)]))
    elif indicator == 'ADOSC':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&fastperiod=5&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'OBV':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'HT_TRENDLINE':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'HT_SINE':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'HT_TRENDMODE':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'HT_DCPERIOD':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'HT_DCPHASE':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    elif indicator == 'HT_PHASOR':
        response = requests.get(
            f'{base_url}function={indicator}&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={api_key}')
        indicator_df = get_response_as_df(response, indicator)
    else:
        print(f'No data was returned for {indicator}')

    test = np.sum(np.array(indicator_df))
    if test > 0:
        return indicator_df
    else:
        pass

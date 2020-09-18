import json
import tensorflow as tf
import io
import zipfile
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np


def transpose_dataframe(data):
    df = pd.DataFrame.from_dict(data)
    prices = df.values
    new = np.zeros(prices.T.shape)
    for i in range(prices.shape[0]):
        row = prices[i, :]
        for j in range(prices.shape[1]):
            value = float(row[-j-1])
            new[j, i] = value
    return new


# YOUR FUNCTION DOES NOT HANDLE ALL THE REQUIRED PARAMETERS NEED TO CHANGE!!!!!
def get_time_series_data(function, symbol, interval, api_key):
    if function == 'TIME_SERIES_INTRADAY':
        base_url = 'https://www.alphavantage.co/query?'
        output_size = 'full'

        response = requests.get(
            f'{base_url}function={function}&symbol={symbol}&interval={interval}&outputsize={output_size}&apikey={api_key}')
        response = response.json()
        data = response[f'Time Series ({interval})']
        df = pd.DataFrame.from_dict(data)
        prices = df.iloc[0, :].values
        prices = [float(prices[-i-1]) for i in range(1, len(prices))]
        prices = pd.DataFrame(prices, columns=[symbol])

    elif function == 'TIME_SERIES_DAILY':
        base_url = 'https://www.alphavantage.co/query?'
        output_size = 'full'

        response = requests.get(
            f'{base_url}function={function}&symbol={symbol}&outputsize={output_size}&apikey={api_key}')
        response = response.json()
        data = response['Time Series (Daily)']
        new = transpose_dataframe(data)

        prices = pd.DataFrame(new, columns=(
            ['daily open', 'daily high', 'daily low', 'daily close', 'daily volume']))

    elif function == 'TIME_SERIES_DAILY_ADJUSTED':
        base_url = 'https://www.alphavantage.co/query?'
        output_size = 'full'

        response = requests.get(
            f'{base_url}function={function}&symbol={symbol}&outputsize={output_size}&apikey={api_key}')
        response = response.json()
        data = response['Time Series (Daily)']
        new = transpose_dataframe(data)

        prices = pd.DataFrame(new, columns=(['daily open', 'daily high', 'daily low', 'daily close',
                                             'daily adjusted close', 'daily volume', 'divident amount', 'split coefficient']))

    elif function == 'TIME_SERIES_WEEKLY':
        base_url = 'https://www.alphavantage.co/query?'
        output_size = 'full'

        response = requests.get(
            f'{base_url}function={function}&symbol={symbol}&apikey={api_key}')
        response = response.json()
        data = response['Weekly Time Series']
        new = transpose_dataframe(data)

        prices = pd.DataFrame(new, columns=(
            ['weekly open', 'weekly high', 'weekly low', 'weekly close', 'weekly volume']))

    elif function == 'TIME_SERIES_WEEKLY_ADJUSTED':
        base_url = 'https://www.alphavantage.co/query?'
        output_size = 'full'

        response = requests.get(
            f'{base_url}function={function}&symbol={symbol}&apikey={api_key}')
        response = response.json()
        data = response['Weekly Adjusted Time Series']
        new = transpose_dataframe(data)

        prices = pd.DataFrame(new, columns=(['weekly open', 'weekly high', 'weekly low',
                                             'weekly close', 'weekly adjusted close', 'weekly volume', 'dividend amount']))

    elif function == 'TIME_SERIES_MONTHLY':
        base_url = 'https://www.alphavantage.co/query?'
        output_size = 'full'

        response = requests.get(
            f'{base_url}function={function}&symbol={symbol}&apikey={api_key}')
        response = response.json()
        data = response['Monthly Time Series']
        new = transpose_dataframe(data)

        prices = pd.DataFrame(new, columns=(
            ['monthly open', 'monthly high', 'monthly low', 'monthly close', 'monthly volume']))

    elif function == 'TIME_SERIES_MONTHLY_ADJUSTED':
        base_url = 'https://www.alphavantage.co/query?'
        output_size = 'full'

        response = requests.get(
            f'{base_url}function={function}&symbol={symbol}&apikey={api_key}')
        response = response.json()
        data = response['Monthly Adjusted Time Series']
        new = transpose_dataframe(data)

        prices = pd.DataFrame(new, columns=(['monthly open', 'monthly high', 'monthly low',
                                             'monthly close', 'monthly adjusted close', "monthly volume", "dividend amount"]))
    return prices

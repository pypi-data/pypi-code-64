import pandas as pd
import numpy as np

df = pd.read_csv(r"https://raw.githubusercontent.com/thecodinguru/lambdata/master/lambdata/example_data/GlobalTemperatures.csv")

def wrangle(df):

  df = df.copy()

  #Drop high cardinality columns to prevent data leakage in the future
  df = df.drop(columns=['LandAverageTemperatureUncertainty', 'LandMaxTemperatureUncertainty',
                        'LandMinTemperatureUncertainty', 'LandAndOceanAverageTemperatureUncertainty' ], axis=1)

  #convert dt column to datetime
  df["dt"] = pd.to_datetime(df["dt"])
  df["Month"] = df["dt"].dt.month
  df["Year"] = df["dt"].dt.year
  df["Day"] = df["dt"].dt.day
  df = df.drop("dt", axis = 1)
  df = df.drop("Month", axis = 1)
  df = df.drop("Day", axis = 1)
  df = df[df.Year >= 1850]

  #set index to Year column
  df = df.set_index(['Year'])

      #convert temps from celsius to fahrenheit so it more readable for Americans
  def convertTemp(x):

    x = float((x * 1.8) + 32)
    return x

  #apply convert function to each column
  df['LandAverageTemperature'] = df['LandAverageTemperature'].apply(convertTemp)
  df['LandMaxTemperature'] = df['LandMaxTemperature'].apply(convertTemp)
  df['LandMinTemperature'] = df['LandMinTemperature'].apply(convertTemp)
  df['LandAndOceanAverageTemperature'] = df['LandAndOceanAverageTemperature'].apply(convertTemp)

  #drop NaN values
  df = df.dropna()

  return df

df1 = wrangle(df)

df1.tail()
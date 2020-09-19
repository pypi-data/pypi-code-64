import pandas as pd
import numpy as np


class TempChange:

    def __init__(self, df, column):
      self.df = df
      self.column = column

    def convertTemp(self):
      DataFrame = pd.DataFrame(data=self.df)
      Columns = pd.Series([self.column])

      for i in Columns:
           i = (i * 1.8) + 32
           return i


  ######EXAMPLE######
df = pd.read_csv(r"https://raw.githubusercontent.com/thecodinguru/lambdata/master/lambdata/example_data/GlobalTemperatures.csv")

#PreCleaning Function
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
  df = df[df.Year >= 2000]

  #set index to Year column
  df = df.set_index(['Year'])


  #drop NaN values
  df = df.dropna()

  return df

df1 = wrangle(df)

#Initilize df2 in TempChange class
LandAverageTemp = TempChange(df1, df1["LandAverageTemperature"])
LandMaxTemp = TempChange(df1, df1["LandMaxTemperature"])
LandMinTemp = TempChange(df1, df1["LandMinTemperature"])
LandAndOceanAverageTemp = TempChange(df1, df1["LandAndOceanAverageTemperature"])

#apply our convertTemp method
convertedLandAverageTemp = LandAverageTemp.convertTemp()
convertedLandMaxTemp = LandMaxTemp.convertTemp()
convertedLandMinTemp = LandMinTemp.convertTemp()
convertedLandAndOceanAverageTemp = LandAndOceanAverageTemp.convertTemp()

df1["LandAverageTemperature"] = convertedLandAverageTemp
df1["LandMaxTemperature"] = convertedLandMaxTemp
df1["LandMinTemperature"] = convertedLandMinTemp
df1["LandAndOceanAverageTemperature"] = convertedLandAndOceanAverageTemp

df1.tail()
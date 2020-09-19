import pandas as pd
import numpy as np
from lambdata import wrangle

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
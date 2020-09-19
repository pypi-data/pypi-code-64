#########################################################################################################
##    pip install lambdata module (if using google colab), use below prior to running code:
##
##    %%capture
##    import sys
##    if 'google.colab' in sys.modules:
##              !pip install lambdata_thecodinguru==0.1.2.*
#########################################################################################################
##    pip install lambdata module (if using juypter notebooks), use below prior to running code:
##
##    !pip install --index-url https://pypi.org/project/lambdata-thecodinguru/
#########################################################################################################
##    if using local/virtual environment, use below in git/command line/powershell prior to running code:
##
##    pipenv install lambdata-thecodinguru
#########################################################################################################


import pandas as pd
import numpy as np

#Read CSV file into pandas DataFrame
globalTempOriginal = pd.read_csv(r"https://raw.githubusercontent.com/thecodinguru/lambdata/master/lambdata/example_data/GlobalTemperatures.csv")

#Call wrangle function from lambdata
import lambdata_thecodinguru as lambdata
globalTempWrangled = lambdata.wrangle(globalTempOriginal)

#Show cleaned dataframe
globalTempWrangled.head()
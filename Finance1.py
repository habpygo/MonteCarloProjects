import pandas as pd
import numpy as np
from pandas_datareader import data as web
import matplotlib.pyplot as plt



goog = web.DataReader('NYSEARCA:GLD', data_source='google', start= '3/14/2009', end= '6/20/2016')
print(goog.tail())

goog['Log_Ret'] = np.log(goog['Close'] / goog['Close'].shift(1))
goog['Volatility'] = pd.rolling_std(goog['Log_Ret'], window=252) * np.sqrt(252)

goog[['Close', 'Volatility']].plot(subplots=True, color='blue', figsize=(8, 6))

plt.show()
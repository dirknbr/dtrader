
# take one of the stocks and then find the feature that correlates most with
# future value

import numpy as np
import pandas as pd
from metrics import *

h = 1

data = pd.read_csv('data.csv')
data2 = pd.pivot_table(data, index=data.time, columns='stock', values='Open')
print(data2)
print(list(data2))
matrix = np.array(data2)
print(matrix.shape)

# loop over ema span, sma span, lookback and horizon
best = 0
stock = 0

for espan in np.arange(1, 21):
  for sspan in np.arange(1, 21):
    for h in np.arange(1, 21):
      y = matrix[:, stock]
      n = len(y)
      ratio = lead(y, h) / y
      rsiy = rsi(y, espan)
      e = ema(y, espan)
      s = sma(y, sspan)
      valid = [i for i in range(sspan, n - h)]
      # corr = np.corrcoef(ratio[valid], (rsiy)[valid])[0, 1]
      corr = np.corrcoef(ratio[valid], (e / s)[valid])[0, 1]
      # print(corr)
      if abs(corr) > best:
        best = abs(corr)
        print(espan, sspan, h, corr)  

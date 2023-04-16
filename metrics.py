
import numpy as np
import pandas as pd

def sma(x, span=1):
  return pd.Series(x).rolling(span).mean()

def ema(x, span=1):
  return pd.Series(x).ewm(span, adjust=False).mean()

def lag(x, l=1):
  return pd.Series(x).shift(l)

def lead(x, l=1):
  return pd.Series(x).shift(-l)

def rsi(x, span=14):
  gain = np.maximum(0, x - lag(x, 1))
  loss = np.maximum(0, lag(x, 1) - x)
  avg_gain = wilder(gain, span)
  avg_loss = wilder(loss, span)
  # rs = avg_gain / avg_loss
  # return 100 - (100 / (1 + rs))
  return 100 * avg_gain / (avg_gain + avg_loss)

# https://tulipindicators.org/wilders
def wilder(x, span=1):
  return pd.Series(x).ewm(alpha=1/span, adjust=False).mean()

if __name__ == '__main__':
  x = np.arange(10)
  print(sma(x, 2))
  print(ema(x, 2))
  print(lag(x, 2))
  print(lead(x, 2))
  print(rsi(x, 2))
  print(wilder(x, 2))
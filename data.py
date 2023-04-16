
import yfinance as yf
import pandas as pd

symbols = 'BIDU MRNA GOOG AAPL KO AMZN GS DIS TSLA NFLX GME V XOM NKE WMT PEP CVX'
histall = None

for symbol in symbols.split(' '):
  print(symbol)
  data = yf.Ticker(symbol)
  hist = data.history(period='2y', interval='1h')
  hist['stock'] = symbol
  hist['time'] = hist.index
  if histall is None:
    histall = hist
  else:
  	histall = histall.append(hist)

print(histall)
histall.to_csv('data.csv')
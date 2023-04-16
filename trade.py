"""

TODO
- fix the nan issue in the value mean
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from masterbot import Bot

CASH = 100000

data = pd.read_csv('data.csv')

STOCKS = len(data.stock.unique())

# https://colab.research.google.com/drive/1j7qE4RxSGAbh6nVQ_Mds2bK9gz4vXhp6#scrollTo=fHLC9F8ZzryB

class Warren(Bot):
  # buys if he doesn't hold, keeps it forever
  def decision(self, stockid, price, time):
    if self.cash > 0:
      if stockid not in self.stock:
        amt = CASH / STOCKS
        qty = amt / price 
        return 'buy', qty
    return '', 0

class Tag(Bot):
  def decision(self, stockid, price, time):
    if time > 8:
      growth = matrix[time, stockid] / matrix[time - 8, stockid] - 1
      if growth < self.pcts[0]:
        amt = min([self.cash, 6000])
        qty = amt / price 
        return 'buy', qty      
      elif growth < self.pcts[1]:
        amt = min([self.cash, 4000])
        qty = amt / price 
        return 'buy', qty
      elif growth > self.pcts[2] and stockid in self.stock:
        qty = self.stock[stockid] / 2
        return 'sell', qty
      elif growth > self.pcts[3] and stockid in self.stock:
        return 'sell', self.stock[stockid]
    return '', 0

class Dirk(Bot):
  def decision(self, stockid, price, time):
    # if price is low buy
    if time > 8:
      growth = matrix[time, stockid] / matrix[time - 8, stockid] - 1
      if growth < -.01:
        amt = self.cash / 20
        qty = amt / price
        return 'buy', qty
    if stockid in self.stock:
      cost_price = self.cost_price_remainder(stockid)
      if price < cost_price * .99:
        amt = self.cash / 20
        qty = amt / price
        return 'buy', qty
      # if make 1% profit sell 25%
      # if make 2% profit sell 50%
      if price > cost_price * 1.01:
        return 'sell', self.stock[stockid] * .25
      elif price > cost_price * 1.02:
        return 'sell', self.stock[stockid] * .5
    return '', 0


# transpose the data into a matrix

data2 = pd.pivot_table(data, index=data.time, columns='stock', values='Open')
print(data2)
print(list(data2))
matrix = np.array(data2)
print(matrix.shape)

warren = Warren()
tag = Tag(pcts=[-.01, -.005, .005, .01])
stunde = Tag(pcts=[-.005, -.0025, .0025, .005])
dirk = Dirk()

bots = [warren, tag, stunde, dirk]

for time in range(matrix.shape[0]):
  for stockid in range(STOCKS):
    price = matrix[time, stockid]
    for bot in bots:
      dec, qty = bot.decision(stockid, price, time)
      if dec == 'buy':
        bot.buy(stockid, price, qty)
      elif dec == 'sell':
        bot.sell(stockid, price, qty)
  prices = matrix[time, :]
  for bot in bots:
    bot.hist_value.append(bot.get_total_value(prices))

for bot in bots:
  print(bot.stock)
  print(bot.hist_value[-1])
  print(min(bot.hist_value), np.nanmedian(bot.hist_value), np.nanmean(bot.hist_value), max(bot.hist_value))

plt.plot(warren.hist_value) 
plt.plot(tag.hist_value) 
plt.plot(stunde.hist_value) 
plt.plot(dirk.hist_value) 
plt.savefig('chart.png')
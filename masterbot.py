CASH = 100000

class Bot:
  def __init__(self, cash=CASH, pcts=None):
    self.cash = cash
    self.hist = {}
    self.stock = {}
    self.hist_value = []
    self.pcts = pcts

  def buy(self, stockid, price, qty):
    amt = price * qty
    if amt <= self.cash:
      self.cash -= amt # reduce cash
      if stockid not in self.stock:
        self.stock[stockid] = 0 # initialise
        self.hist[stockid] = [] 
      self.stock[stockid] += qty
      self.hist[stockid].append(['buy', price, qty, amt])

  def sell(self, stockid, price, qty):
    amt = price * qty
    if self.stock[stockid] >= qty:
      self.stock[stockid] -= qty
      self.cash += amt
      self.hist[stockid].append(['sell', price, qty, amt])

  def get_total_value(self, prices):
    stockids = self.stock.keys()
    return self.cash + sum([self.stock[i] * prices[i] for i in stockids])

  def avg_price_bought(self, stockid):
    prices = [h[1] for h in self.hist[stockid] if h[0] == 'buy']
    return np.mean(prices)

  def cost_price_remainder(self, stockid):
    sum_qty_bought, sum_qty_sold = 0, 0
    sum_amt_bought, sum_amt_sold = 0, 0
    for item in self.hist[stockid]:
      if item[0] == 'buy':
        sum_qty_bought += item[2]
        sum_amt_bought += item[3]
      else:
        sum_qty_sold += item[2]
        sum_amt_sold += item[3]
    rem_qty = sum_qty_bought - sum_qty_sold # this should match self.stock
    rem_amt = sum_amt_bought - sum_amt_sold
    return rem_amt / rem_qty

if __name__ == '__main__':
  bot = Bot()
  bot.buy(0, 100, 100)
  bot.sell(0, 120, 50)
  print(bot.hist)
  # expect 4000 / 50 = 80
  print(bot.cost_price_remainder(0))
  print(bot.cash) 
  print(bot.get_total_value([100])) 
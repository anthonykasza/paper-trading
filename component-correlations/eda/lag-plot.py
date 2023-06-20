import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

from tickers import all_tickers, qqq
from get_data import get_data
tickers = qqq[0:1]
df, start_day, end_day = get_data()


Xs = defaultdict(list)
delta = timedelta(days=1)
skip = True
yesterdays = defaultdict(list)
while start_day <= end_day:

  # skip weekends
  if len(df['Close'][tickers[0]][str(start_day)]) == 0:
    start_day += delta
    continue

  for ticker in tickers:
    p_close = np.array(df['Close'][ticker][str(start_day)])
    if math.isnan(p_close[0]):
      continue
    p_high = np.array(df['High'][ticker][str(start_day)])
    p_low = np.array(df['Low'][ticker][str(start_day)])
    p = (p_close - p_low) / (p_high - p_low)
    Xs[ticker].extend(p)

  skip = False
  start_day += delta

size = 7
fig, axs = plt.subplots(size, size)
lag = size ** 2
col = row = 0
while lag > 0:
  if row > size-1:
    row = 0
    col += 1
  for ticker,prices in Xs.items():
    X = pd.Series(Xs[ticker], range(len(Xs[ticker])))
    pd.plotting.lag_plot(X, lag=lag, ax=axs[row, col%size])
  row += 1
  lag -= 1

fig.suptitle(qqq[0])
plt.show()

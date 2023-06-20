import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

from tickers import all_tickers, qqq
from get_data import get_data
tickers = qqq[:5]
df, start_day, end_day = get_data()

Xs_per = defaultdict(list)
Xs_high_low_ratio = defaultdict(list)
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
    p_open = np.array(df['Open'][ticker][str(start_day)])
    p_high = np.array(df['High'][ticker][str(start_day)])
    p_low = np.array(df['Low'][ticker][str(start_day)])
    Xs_high_low_ratio[ticker].extend((p_close - p_low) / (p_high - p_low))
    Xs[ticker].extend(p_close)

    if skip:
      Xs_per[ticker].extend([0]*len(p_close))
    else:
      Xs_per[ticker].extend((p_close - yesterdays[ticker]) / yesterdays[ticker])
    yesterdays[ticker] = p_close

  skip = False
  start_day += delta
  print(start_day)

fig, axs = plt.subplots(3, 1)
for ticker,prices in Xs_high_low_ratio.items():
  axs[0].plot(range(len(prices)), prices, label=ticker)
for ticker,prices in Xs.items():
  axs[1].plot(range(len(prices)), prices, label=ticker)
for ticker,prices in Xs_per.items():
  axs[2].plot(range(len(prices)), prices, label=ticker)

axs[0].set_title('Normalized')
axs[0].legend()
axs[1].set_title('Raw Prices')
axs[1].legend()
axs[2].set_title("Percent of Yesterday's Price")
axs[2].legend()
plt.show()

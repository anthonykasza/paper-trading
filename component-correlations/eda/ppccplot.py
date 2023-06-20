import math
import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

from tickers import all_tickers, qqq
from get_data import get_data
tickers = qqq[0:1]
df, start_day, end_day = get_data()

Xs_high_low_ratio = defaultdict(list)
delta = timedelta(days=1)
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

  start_day += delta
  print(start_day)

fig, axs = plt.subplots(3, 1)
for ticker,prices in Xs_high_low_ratio.items():
  scipy.stats.ppcc_plot(prices, a=min(prices), b=max(prices), dist='tukeylambda', plot=axs[0])
  scipy.stats.ppcc_plot(prices, a=min(prices), b=max(prices), dist='lognorm', plot=axs[1])
  scipy.stats.ppcc_plot(prices, a=min(prices), b=max(prices), dist='gamma', plot=axs[2])

axs[0].set_title('tukeylambda')
axs[0].legend()
axs[1].set_title('lognorm')
axs[1].legend()
axs[2].set_title('gamma')
axs[2].legend()
plt.show()

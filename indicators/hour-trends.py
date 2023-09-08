import scipy
import os
import random
import pickle
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

weak_ass_slopes = True

def get_data(ticker, data_path="data.pkl", num_of_days=10):
  if os.path.isfile(data_path):
    file = open(data_path, 'rb')
    df = pickle.load(file)
    file.close()
  else:
    end_day = (datetime.today() - timedelta(days=1))
    start_day = (datetime.today() - timedelta(days=num_of_days))
    data = yf.download(ticker, start=start_day.strftime('%Y-%m-%d'), end=end_day.strftime('%Y-%m-%d'), interval='15m')
    df = pd.DataFrame(data)
    file = open(data_path, 'wb')
    pickle.dump(df, file)
    file.close()
  return df

# Sept 1-8: ups from open to 10am, downs from 10am to 11am
df = get_data(ticker="XOM")
signal = df['Close']

start_day, end_day = df.index.min(), df.index.max()
current_day = start_day
day_list = []
while current_day <= end_day:
  try:
    print(signal[current_day.strftime('%Y-%m-%d')][0])
    day_list.append(current_day)
  except:
    print("  no data", current_day.strftime('%Y-%m-%d'))
  current_day += timedelta(days=1)

fig, ax = plt.subplots(len(day_list), figsize=(12, 6))
hour_sentiment = defaultdict(int)
for day_idx in range(len(day_list)):
  day = day_list[day_idx]
  day_signal = signal[day.strftime('%Y-%m-%d')]

  if len(day_signal.index) > 1:
    for hour in [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7)]:
      start_h = (4 * hour[0]) - 2
      if start_h < 0:
        start_h = 0
      stop_h = (4 * hour[1]) - 2
      if stop_h >= len(day_signal.index):
        stop_h -= 1
      ax[day_idx].axvline(day_signal.index[start_h])
      ax[day_idx].axvline(day_signal.index[stop_h])
      ax[day_idx].text(day_signal.index[start_h], max(day_signal), str(hour[0]+9))
      hour_signal = [each for each in day_signal[start_h:stop_h]]
      res = scipy.stats.linregress(range(len(hour_signal)), hour_signal)
      if weak_ass_slopes:
        if res.slope > 0:
          hour_sentiment[hour] += 1
          ax[day_idx].axvspan(day_signal.index[start_h], day_signal.index[stop_h], alpha=0.5, color='green')
        else:
          hour_sentiment[hour] -= 1
          ax[day_idx].axvspan(day_signal.index[start_h], day_signal.index[stop_h], alpha=0.5, color='red')
      else:
        if res.slope >= 0.15:
          hour_sentiment[hour] += 1
          ax[day_idx].axvspan(day_signal.index[start_h], day_signal.index[stop_h], alpha=0.5, color='green')
        elif res.slope < 0.15 and res.slope > -0.15:
          ax[day_idx].axvspan(day_signal.index[start_h], day_signal.index[stop_h], alpha=0.5, color='gray')
        else:
          hour_sentiment[hour] -= 1
          ax[day_idx].axvspan(day_signal.index[start_h], day_signal.index[stop_h], alpha=0.5, color='red')
    ax[day_idx].plot(day_signal.index, day_signal)

print(hour_sentiment)
plt.show()

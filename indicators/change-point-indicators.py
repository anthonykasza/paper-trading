# props:
#  - https://github.com/sztistvan/change_detection
#  - https://www.r-bloggers.com/2023/04/building-and-backtesting-a-volatility-based-trading-strategy-with-chatgpt/
#
# chatgpt is cool and all but its hallucinations are troublesome, e.g. the bcp python module.

import os
import scipy
import random
import pickle
import numpy as np
import pandas as pd
import yfinance as yf
import ruptures as rpt
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def get_data(ticker, data_path="data.pkl", num_of_days=365*3):
  # check to see if there's a cache on disk and read from it
  if os.path.isfile(data_path):
    file = open(data_path, 'rb')
    df = pickle.load(file)
    file.close()
  # if there's no cache, Grab it from the API and write it to disk
  else:
    end_day = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_day = (datetime.today() - timedelta(days=num_of_days)).strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start_day, end=end_day)
    df = pd.DataFrame(data)
    file = open(data_path, 'wb')
    pickle.dump(df, file)
    file.close()
  return df


def detect_changes(time_series):
  signal = time_series.values
  # tune jump value?
  algo = rpt.Pelt(model="rbf", min_size=1, jump=10).fit(signal)
  result = algo.predict(pen=2)
  change_points = [i for i in result if i < len(signal)]
  return change_points


# Get ticker price data and calculate means and std dev
df = get_data(ticker="GOOG")
signal = df['Adj Close']
changes = detect_changes(signal)
# tune lookback window?
lookback_window = 10
# center=True would introduce a look-ahead bias
rolling_mean = signal.rolling(window=lookback_window, center=False).mean()
rolling_std = signal.rolling(window=lookback_window, center=False).std()
upper = rolling_mean + (2*rolling_std)
lower = rolling_mean - (2*rolling_std)


# Plot price, mean, and std dev
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(signal, label='close price', color='blue')
ax.plot(rolling_mean, color='orange', label='mean')
ax.plot(upper, color='green', label='2 std dev')
ax.plot(lower, color='green')
plt.fill_between(signal.index, upper, lower, alpha=0.25, color='green')
ax.set_xlabel('Time')
ax.set_ylabel('Price')
ax.set_title('BUY/SELL Indicators Based on Mean-Reversion and Change Point Detection')

# we use the slope of the rolling mean to indicate a BUY or SELL
#  this makes some assumptions but we're using it for simplicity
#  at each changepoint we look backwards to determine the slope of 5 different
#  trend durations. we weight each duration, favoring shorter durations then sum
#  the weighted values into an overall sentiment/indicator
for i in changes:

  action = ""
  weight = 0
  # Tune lookback weights?
  weight_table = {"1yr":0.036219, "6mo":0.069814, "3mo":0.13457, "1mo":0.259395, "1w":0.5}
  for duration_name, duration in {"1yr": 365, "6mo": 182, "3mo": 91, "1mo": 30, "1w":7}.items():
    if duration > i:
      duration = i - lookback_window
    lookback = rolling_mean[i-duration:i]
    res = scipy.stats.linregress(range(len(lookback)), lookback)
    weight += res.slope * weight_table[duration_name]
    if res.slope > 0:
      action = action + str(round(res.slope, 2)) + "_BUY_" + duration_name + "\n"
    else:
      action = action + str(round(res.slope, 2)) + "_SELL_" + duration_name + "\n"

  if weight > 0:
    action += str(round(weight, 2)) + "_BUY_WEIGHTED"
  else:
    action += str(round(weight, 2)) + "_SELL_WEIGHTED"

  ax.axvline(signal.index[i], color='red', linestyle='--')
  y = random.randint(int(signal.min()), int(signal.mean()))
  ax.text(signal.index[i], y, action, color='red')


# If the price goes outside of 2 stddev from the rolling mean,
#  we assume it will revert to the mean "soon". at each breakout
#  we determine how far into the future we would have been correct
for idx in range(len(signal)):
  bag_holdin = True

  if signal[idx] > upper[idx]:
    action = "SELL_"
    for idx2 in range(len(signal[idx:])):
      if signal[idx+idx2] < signal[idx]:
        action = action + str(idx2) + "_days_until_flat"
        bag_holdin = False
        break
    if bag_holdin:
      action += "YOU_ARE_STILL_BAG_HOLDIN'"
      bag_holdin = False
    plt.scatter(signal.index[idx], signal[idx], color="purple")
    ax.text(signal.index[idx], signal[idx], action, rotation=45)

  if signal[idx] < lower[idx]:
    action = "BUY_"
    for idx2 in range(len(signal[idx:])):
      if signal[idx+idx2] > signal[idx]:
        action = action + str(idx2) + "_days_until_flat"
        bag_holdin = False
        break
    if bag_holdin:
      action += "YOU_ARE_STILL_BAG_HOLDIN'"
      bag_holdin = False
    plt.scatter(signal.index[idx], signal[idx], color="purple")
    ax.text(signal.index[idx], signal[idx], action, rotation=45)


ax.legend()
plt.show()

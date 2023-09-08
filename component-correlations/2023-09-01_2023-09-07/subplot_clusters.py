from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from random_colors import rand_cmap
from get_data import get_data

df, start_day, end_day = get_data()

ticker_symbols = []
cluster_labels = []
with open('clusters', 'r') as f:
  for line in f:
    t, c = line.strip().split()
    ticker_symbols.append(t)
    c = int(c)
    cluster_labels.append(c)

prices = []
for ticker in ticker_symbols:
  p_close = df['Close'][ticker]
  p_open = df['Open'][ticker]
  p_high = df['High'][ticker]
  p_low = df['Low'][ticker]
  ratio = (p_close - p_low) / (p_high - p_low)
  prices.append(ratio[~np.isnan(ratio)])


data = defaultdict(list)
for idx in range(len(ticker_symbols)):
  symbol = ticker_symbols[idx]
  cluster = cluster_labels[idx]
  price = prices[idx]
  data[cluster].append(price)

fig, ax = plt.subplots(len(data.keys()), figsize=(9, 6))
ax_count = 0
for cluster,prices in data.items():
  if cluster == -1: # skip noise
    continue
  for price in prices:
    ax[ax_count].plot(price.index.strftime('%Y-%m-%d %H:%M:%S'), price.values, label=price.name)
    ax[ax_count].legend()
  ax[ax_count].set_title("Cluster " + str(cluster))
  ax_count += 1
plt.savefig('cluster_subplots.png')

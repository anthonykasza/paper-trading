# this is pretty neat, too: https://www.kaggle.com/code/aavigan/ecg-classification-using-fastdtw/notebook

import numpy as np
from dtaidistance import dtw
import matplotlib.pyplot as plt
import hdbscan
from sklearn.neighbors import NearestNeighbors
from random_colors import rand_cmap


from tickers import all_tickers, qqq
from get_data import get_data
tickers = qqq[:] + ["QQQ"]
df, start_day, end_day = get_data()

price_data = []
for ticker in tickers:
  p_close = df['Close'][ticker]
  p_open = df['Open'][ticker]
  p_high = df['High'][ticker]
  p_low = df['Low'][ticker]
  ratio = (p_close - p_low) / (p_high - p_low)
  price_data.append(ratio[~np.isnan(ratio)])

# building this matrix could be made 2x faster as its just a mirror
#  along the diagonal
pairwise_distances = []
for idx1 in range(len(tickers)):
  ratio_row = []
  for idx2 in range(len(tickers)):
    p1 = price_data[idx1]
    p2 = price_data[idx2]
    distance = dtw.distance(p1, p2)
    ratio_row.append(distance)
  pairwise_distances.append(ratio_row)


# min_cluster_size is 2, we're looking for pairs
params = {'metric':'precomputed', 'min_cluster_size':2, 'min_samples':1}
clusterer = hdbscan.HDBSCAN(**params)
distance_matrix = np.array(pairwise_distances)
clusterer.fit(distance_matrix)
labels = clusterer.labels_

cmap = rand_cmap(100, type='bright', first_color_black=True, last_color_black=False, verbose=False)
fig, ax = plt.subplots()
for idx in range(len(price_data)):
  series = price_data[idx]
  ax.plot(series.index, series.values, label=series.name, c=cmap(labels[idx]))
  print(series.name, labels[idx])
ax.set_title("Price Ratio Time Series Clusters")
plt.show()

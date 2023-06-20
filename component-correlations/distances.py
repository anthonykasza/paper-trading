import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

from dtaidistance import dtw

from tickers import all_tickers, qqq
from get_data import get_data
tickers = qqq[:] + ["QQQ"]
df, start_day, end_day = get_data()


# pairwise distances measure how far a single ticker's price movements are from a second ticker's price movements
pairwise_distances = defaultdict(list)

# global distances measure how far a single ticker's price movements are from ALL other tickers' price movements
global_distances = defaultdict(list)

days = []
delta = timedelta(days=1)
while start_day <= end_day:

  # skip weekends
  if len(df['Close'][tickers[0]][str(start_day)]) == 0:
    start_day += delta
    continue

  for t1 in tickers:
    for t2 in tickers:
      # skip some pairs because (a,b) is the same as (b,a)
      # NOTE: we still do self-comparisons (qqq,qqq) because they influence normalization
      if t1 < t2:
        continue

      # this day's close prices
      pair = (t1, t2)
      p1 = np.array(df['Close'][t1][str(start_day)])
      p2 = np.array(df['Close'][t2][str(start_day)])

      # normalize price movement around the day's mean
      p1 = [each/p1.mean() for each in p1]
      p2 = [each/p2.mean() for each in p2]

      # find the dtw distance between 2 tickers' normalized price movements for a single day
      distance = dtw.distance(p1, p2)
      # skip days with no data
      if math.isnan(distance):
        continue
      pairwise_distances[pair].append(distance)

      # each ticker receives half of the distance
      half = distance / 2
      global_distances[t1].append(half)
      global_distances[t2].append(half)

  days.append(start_day)
  start_day += delta
  print(start_day)

####
# average across days and normalize across entire population
global_distances = {k:np.array(v).mean() for k,v in global_distances.items()}
gmax = np.array([v for v in global_distances.values()]).max()
gmin = np.array([v for v in global_distances.values()]).min()
global_distances = {k:((v-gmin)/(gmax-gmin)) for k,v in global_distances.items()}

pairwise_distances = {k:np.array(v).mean() for k,v in pairwise_distances.items()}
pmax = np.array([v for v in pairwise_distances.values()]).max()
pmin = np.array([v for v in pairwise_distances.values()]).min()
pairwise_distances = {k:((v-pmin)/(pmax-pmin)) for k,v in pairwise_distances.items()}

####
# dump results to flat files
with open('pairwise_distances', 'w') as f:
  for k,v in pairwise_distances.items():
    s = "{}\t{}\t{}\n".format(k[0], k[1], v)
    f.write(s)

global_distances = sorted(global_distances.items(), key=lambda x:x[1])
with open('global_distances', 'w') as f:
  for (k,v) in global_distances:
    s = "{}\t{}\n".format(k,v)
    f.write(s)


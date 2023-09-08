import matplotlib.pyplot as plt

X = []
Y = []
with open('pairwise_distances', 'r') as f:
  for line in f:
    t1, t2, d = line.strip().split("\t")
    d = float(d)
    X.append(d)

plt.hist(X, bins=250)
plt.title("distribution of distances between 2 tickers.\nthe zeros are tickers compared against themselves")
plt.savefig('pairwise.png')

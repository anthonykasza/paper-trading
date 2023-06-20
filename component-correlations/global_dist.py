import matplotlib.pyplot as plt

X = []
Y = []
with open('global_distances', 'r') as f:
  for line in f:
    t, d = line.strip().split("\t")
    d = float(d)
    X.append(d)

plt.hist(X, bins=20)
plt.title("distribution of ticker's distances from all other tickers\n90% are less than 0.4")
plt.show()


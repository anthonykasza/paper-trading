import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.datasets as data
import hdbscan
from sklearn.metrics.pairwise import pairwise_distances

sns.set_context('poster')
sns.set_style('white')
sns.set_color_codes()
moons, _ = data.make_moons(n_samples=50, noise=0.05)
blobs, _ = data.make_blobs(n_samples=50, centers=[(-0.75,2.25), (1.0, 2.0)], cluster_std=0.25)
test_data = np.vstack([moons, blobs])
distance_matrix = pairwise_distances(test_data)
clusterer = hdbscan.HDBSCAN(metric='precomputed')
clusterer.fit(distance_matrix)
labels = clusterer.labels_

fig, ax = plt.subplots()
plot_kwds = {'alpha' : 0.5, 's' : 80, 'linewidths':0, 'cmap':"Spectral", 'c':labels}
scatter = ax.scatter(test_data.T[0], test_data.T[1], **plot_kwds)
legend = ax.legend(*scatter.legend_elements(num=len(set(labels))), loc="upper right", title="Cluster")
ax.add_artist(legend)
print(labels)
plt.show()

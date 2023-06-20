import numpy as np
from dtaidistance import dtw

p1 = np.array([0])
p2 = np.array([0])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0])
p2 = np.array([1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0,0,0])
p2 = np.array([1,1,1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0,0,0])
p2 = np.array([1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0,0,0])
p2 = np.array([1,1,1,1,1,1,])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0,0,0,0,0,0])
p2 = np.array([1,1,1,1,1,1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0])
p2 = np.array([1,1,1,1,1,1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0,0,1,0,0,0])
p2 = np.array([1,1,1,1,1,1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0,0,0,0,0,1])
p2 = np.array([1,1,1,1,1,1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([0,0,1,0,0,1])
p2 = np.array([1,1,1,1,1,1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([1,0,1,0,0,1])
p2 = np.array([1,1,1,1,1,1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

p1 = np.array([1,0,1,1,1,1])
p2 = np.array([1,1,1,1,1,1])
distance = dtw.distance(p1, p2)
print(distance, p1, p2)

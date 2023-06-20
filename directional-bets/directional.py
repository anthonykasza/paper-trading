import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


data = pd.read_csv('data', sep=' ', header=0)
Y = (data['PriceClose'] - data['Strike']) / data['PriceOpen']
X = range(0, len(Y))
threshold = 0.19

# Split trade errors
X_put_otm = []
Y_put_otm = []
X_put_itm = []
Y_put_itm = []
X_call_otm = []
Y_call_otm = []
X_call_itm = []
Y_call_itm = []
for idx in range(len(X)):
  # puts
  if data['Type'][idx] == 'P':
    # otm
    if Y[idx] >= 0:
      X_put_otm.append(X[idx])
      Y_put_otm.append(Y[idx])
    # itm
    else:
      X_put_itm.append(X[idx])
      Y_put_itm.append(Y[idx])
  # calls
  else:
    # otm
    if Y[idx] <= 0:
      X_call_otm.append(X[idx])
      Y_call_otm.append(Y[idx])
    # itm
    else:
      X_call_itm.append(X[idx])
      Y_call_itm.append(Y[idx])


fig, ax = plt.subplots()
ax.scatter(X_call_itm, Y_call_itm, c="blue", label="Call ITM")
ax.scatter(X_put_itm, Y_put_itm, c="red", label="Put ITM")
ax.scatter(X_call_otm, Y_call_otm, c="skyblue", label="Call OTM")
ax.scatter(X_put_otm, Y_put_otm, c="pink", label="Put OTM")
ax.set_xlabel("Trade Count")
ax.set_ylabel("Error Magnitude (as a percent of price)")
plt.grid(visible=True)
plt.title("Directional Errors")
plt.legend()
plt.show()


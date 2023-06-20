
"""
Weights assume a bull market overall trend - sell calls OTM, prefer to hold stock

PUT-ITM, 3/10, red
The PUT you sold is (deep) in-the-money.
You had to over pay for the underlying and may need to wait a month or more for the price to recover.

PUT-ITM-ATM, 10/10, green
The PUT you sold is barely in-the-money.
You overpaid slightly for the underlying; take assignment and sell a OTM-ATM or OTM CALL.

PUT-OTM-ATM, 7/10, lightgreen
The PUT you sold is barely out-of-the-money.
Sell another PUT near OTM-ATM since this is a Bull Market.

PUT-OTM, 4/10, yellow
The PUT you sold is (deep) out-of-the-money.
You're strike selection was too conservative and suffered opportunity loss. Sell another PUT closer to OTM-ATM.

CALL-OTM, 3/10, red
The CALL you sold is (deep) out-of-the-money.
You're strike selection was too conservative and you suffered opportunity loss. You also lost on the underlying assuming you sold the call covered.

CALL-OTM-ATM, 10/10, green
The CALL you sold was barely out-of-the-money.
Sell another CALL farther OTM.

CALL-ITM-ATM, 8/10, lightgreen
The CALL you sold was barely in-the-money.
Buy the underlying and sell another OTM covered CALL or sell a ATM-OTM PUT.

CALL-ITM, 4/10, yellow
The CALL you sold was (deep) in-the-money.
You're strike selection was too conservative and you suffered opportunity loss. 
Buy the underlying and sell another OTM covered CALL or sell a ATM-OTM PUT.
"""

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
put_otm_colors = []
X_put_itm = []
Y_put_itm = []
put_itm_colors = []
X_call_otm = []
Y_call_otm = []
call_otm_colors = []
X_call_itm = []
Y_call_itm = []
call_itm_colors = []
for idx in range(len(X)):
  # puts
  if data['Type'][idx] == 'P':
    # otm
    if Y[idx] >= 0:
      X_put_otm.append(X[idx])
      Y_put_otm.append(Y[idx])
      # PUT-OTM
      if Y[idx] >= threshold:
        put_otm_colors.append('yellow')
      # PUT-OTM-ATM
      else:
        put_otm_colors.append('lightgreen')
    # itm
    else:
      X_put_itm.append(X[idx])
      Y_put_itm.append(Y[idx])
      # PUT-ITM
      if Y[idx] <= threshold * -1:
        put_itm_colors.append('red')
      # PUT-ITM-ATM
      else:
        put_itm_colors.append('green')
  # calls
  else:
    # otm
    if Y[idx] <= 0:
      X_call_otm.append(X[idx])
      Y_call_otm.append(Y[idx])
      # CALL-OTM
      if Y[idx] <= threshold * -1:
        call_otm_colors.append('red')
      # CALL-OTM-ATM
      else:
        call_otm_colors.append('green')
    # itm
    else:
      X_call_itm.append(X[idx])
      Y_call_itm.append(Y[idx])
      # CALL-ITM
      if Y[idx] >= threshold:
        call_itm_colors.append('yellow')
      # CALL-ITM-ATM
      else:
        call_itm_colors.append('lightgreen')


fig, ax = plt.subplots()
ax.scatter(X_call_itm, Y_call_itm, c=call_itm_colors, marker="*", label="Call ITM")
ax.scatter(X_put_itm, Y_put_itm, c=put_itm_colors, marker="o", label="Put ITM")
ax.scatter(X_call_otm, Y_call_otm, c=call_otm_colors, marker="x", label="Call OTM")
ax.scatter(X_put_otm, Y_put_otm, c=put_otm_colors, marker="d", label="Put OTM")
ax.set_xlabel("Trade Count")
ax.set_ylabel("Error Magnitude (as a percent of price)")
plt.grid(visible=True)
plt.title("Trades Ranked by Directional Outcome assuming a Bull Market")

handles = []
label_list = [
  ("Bad, PUT-ITM", "o", "red"),
  ("Great, PUT-ITM-ATM", "o", "green"),
  ("OK, PUT-OTM", "d", "yellow"),
  ("Good, PUT-OTM-ATM", "d", "lightgreen"),
  ("OK, CALL-ITM", "*", "yellow"),
  ("Good, CALL-ITM-ATM", "*", "lightgreen"),
  ("Bad, CALL-OTM", "x", "red"),
  ("Great, CALL-OTM-ATM", "x", "green")]
for tup in label_list:
  (l, m, c) = tup
  handles.append(mlines.Line2D([], [], color=c, marker=m, linestyle='None', markersize=10, label=l))
plt.legend(handles=handles)

plt.show()


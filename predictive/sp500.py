# Wow. Thank you, Vik!
#  https://www.youtube.com/watch?v=1O_BenficgE
#  https://github.com/dataquestio/project-walkthroughs/blob/master/sp_500/market_prediction.ipynb

import os
import pandas as pd
import yfinance as yf
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


# TODO - feature engineer more predictor columns like:
#   SP500 RSI, VIX, NASDAQ ratios/trends, BTC, the Agg, jobless claims, GDP, PCE

def get_data():
  try:
    if os.path.exists("sp500.csv"):
      sp500 = pd.read_csv("sp500.csv", index_col=0)
    else:
      sp500 = yf.Ticker("^GSPC")
      sp500 = sp500.history(period="max")
      sp500.to_csv("sp500.csv")
  except:
    print("Failed getting data")
    exit()
  sp500.index = pd.to_datetime(sp500.index, utc=True)
  sp500["Tomorrow"] = sp500["Close"].shift(-1)
  sp500["Target"] = (sp500["Tomorrow"] > sp500["Close"]).astype(int)
  sp500 = sp500.loc["2005-01-01":].copy()
  return sp500


def predict(train, test, predictors, model, confidence):
  model.fit(train[predictors], train["Target"])
  preds = model.predict_proba(test[predictors])[:,1]
  preds[preds >= confidence] = 1
  preds[preds < confidence] = 0
  preds = pd.Series(preds, index=test.index, name="Predictions")
  combined = pd.concat([test["Target"], preds], axis=1)
  return combined


def backtest(data, model, predictors, confidence=0.50, start=250*5, step=250):
  all_predictions = []
  for i in range(start, data.shape[0], step):
    train = data.iloc[0:i].copy()
    test = data.iloc[i:(i+step)].copy()
    predictions = predict(train, test, predictors, model, confidence)
    all_predictions.append(predictions)
  return pd.concat(all_predictions)


def howd_we_do(predictions):
  print(predictions["Predictions"].value_counts())
  print(precision_score(predictions["Target"], predictions["Predictions"]))
  print(predictions["Target"].value_counts() / predictions.shape[0])


# GET HISTORIC DATA
sp500 = get_data()

# MUNGE DATA - CALCULATE RATIOS AND TRENDS
horizons = [1, 7, 14, 30, 90, 180, 365]
predictors = []
for horizon in horizons:
  # TODO - consider different methods of smoothing, SMA vs EMA
  rolling_averages = sp500.rolling(horizon).mean()

  ratio_column = f"Close_Ratio_{horizon}"
  sp500[ratio_column] = sp500["Close"] / rolling_averages["Close"]
  predictors += [ratio_column]

  trend_column = f"Trend_{horizon}"
  sp500[trend_column] = sp500.shift(1).rolling(horizon).sum()["Target"]
  predictors += [trend_column]

sp500 = sp500.dropna(subset=sp500.columns[sp500.columns != "Tomorrow"])


# SEARCH FOR OPTIMAL PARAMS TO RANDOMFOREST
param_grid = {
  'n_estimators': [50, 100, 200, 300],
  'min_samples_split': [5, 10, 50, 100, 200],
  'min_samples_leaf': [1, 2, 5, 10, 50],
}
base_model = RandomForestClassifier(random_state=1)
grid_search = GridSearchCV(estimator=base_model, param_grid=param_grid, cv=3, n_jobs=-1, scoring='precision')
grid_search.fit(sp500[predictors], sp500["Target"])
best_model = grid_search.best_estimator_

# BACKTEST AND MEASURE
for confidence in [0.30, 0.40, 0.50, 0.60, 0.70]:
  predictions = backtest(sp500, best_model, predictors, confidence=confidence)
  print("{} activision".format(confidence))
  howd_we_do(predictions)
  print()

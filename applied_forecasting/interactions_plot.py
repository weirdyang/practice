import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import scipy.stats as stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
from matplotlib.patches import Ellipse
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (accuracy_score, mean_absolute_error,
                             mean_squared_error, r2_score)
from sklearn.model_selection import KFold, train_test_split
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import summary_table
from sklearn.model_selection import cross_val_predict

df = pd.read_csv('P1training_v5.csv', parse_dates=True, index_col=0)
train, test = train_test_split(df, test_size=0.2, random_state=2)
print(train.head())
test.head()
# lights + RH_1 + T2 + RH_2 + T3 + T4 + T8 + RH_8 + T9 + hour +
formula = 'Appliances ~  C(day_or_night)'
model = smf.ols(formula, data=train).fit()
print(model.summary())
print(model.params)
feats = ['lights', 'RH_1', 'T2', 'RH_2', 'T3', 'T4', 'T8', 'RH_8', 'T9', 'hour', 'day_or_night']
test['y_pred'] = model.predict(test['day_or_night'])
print('RMSE:', np.sqrt(mean_squared_error(test['y_pred'], test['Appliances'])))
fig4, ax = plt.subplots()
test.Appliances.plot(ax=ax, style='b-')
# same ax as above since it's automatically added on the right
test.y_pred.plot(ax=ax, style='r-')
#plt.show()


# instantiate model
lm = LinearRegression()
# check cross validation predictions, 10 splits
feats = ['lights', 'RH_1', 'T2', 'RH_2', 'T3', 'T4', 'T8', 'RH_8', 'T9', 'hour', 'time_of_day_N', 'time_of_day_D']
cv_predictions = cross_val_predict(lm, df[feats], df['Appliances'], cv=10)

fig3 = plt.figure(figsize=(6,6))
plt.scatter(x=cv_predictions, y=df['Appliances'])
df['predictions'] = cv_predictions
# plotting fit results
fig4, ax = plt.subplots()
df.Appliances.plot(ax=ax, style='b-')
# same ax as above since it's automatically added on the right
df.predictions.plot(ax=ax, style='r-')
 # check errors
print('MAE:', mean_absolute_error(df['Appliances'], cv_predictions))
print('RMSE:', np.sqrt(mean_squared_error(df['Appliances'], cv_predictions)))
print('R-Squared:', r2_score(df['Appliances'],cv_predictions))
#plt.show()



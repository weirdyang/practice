
import matplotlib.pyplot as plt
import numpy as np
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
# scikit learn
# load df
# reading and loading into dataframe
df = pd.read_csv('P1training.csv')
df['date'] = pd.to_datetime(df['date'])
df['hour'] = pd.to_datetime(df['date']).dt.hour
df.head()

# split into test train:
# determine predictors
feature_cols = [col for col in df.columns if 'Appliances' not in col]
# dependent variables aka response
y = df['Appliances']
# predictors
x = df[feature_cols]
# split data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)

SVR = ['T1', 'T3', 'T4', 'T8', 'T9']
LinearSVC = ['RH_1', 'RH_2', 'T3', 'T8', 'T9', 'lights']
LinearReg = ['RH_1', 'T2', 'RH_2', 'T3', 'T9', 'lights']
kbest_f = ['lights', 'T2', 'T6', 'hour', 'RH_out']
guess = ['lights', 'hour', 'RH_6','T1']
all = [col for col in feature_cols if 'date' not in col]
total_list = [SVR, LinearSVC, LinearReg, kbest_f, guess, all]

def check_rmse(df, response, list_of_list):
    for item in list_of_list:
        cols = item
        print('\nUsing scikit:\n')
        # instantiate model
        lm = LinearRegression()
        # fit model
        lm.fit(X_train[cols], y_train)
        # make predictions
        y_pred = lm.predict(X_test[cols])
        print('MAE:', mean_absolute_error(y_test, y_pred))
        print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
        print('R-Squared:', r2_score(y_test, y_pred))
        print('Score', lm.score(X_test[cols], y_test))

        print('\nUsing statsmodels:\n')
        formula = "{0} ~ {1}".format(response, '+'.join(cols))
        print(formula)
        model = smf.ols(formula, data=df).fit()
        y_pred = model.predict(X_test[cols])
        print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
        print(model.params)
        print(model.summary())
        print('\nCHECKING RESIDUALS\n')
        res = model.resid
        f1 = plt.figure(figsize=(6,6))
        f1 = plt.hist(model.resid_pearson)
        f1 = plt.ylabel('Count')
        f1 = plt.xlabel('Normalized residuals')
        # normality check
        fig = plt.figure(figsize=(6,6))
        fig = sm.qqplot(res, stats.distributions.norm, line='r')
        #plt.show()

        print("\nCross validation using scikit:\n")
        # check cross validation predictions, 10 splits
        cv_predictions = cross_val_predict(lm, df[cols], df[response], cv=10)
        # check errors
        print('MAE:', mean_absolute_error(df[response], cv_predictions))
        print('RMSE:', np.sqrt(mean_squared_error(cv_predictions, df[response])))
        print('R-Squared:', r2_score(cv_predictions, df[response]))
        #print('Score', accuracy_score(df[response], cv_predictions))
        # plot
        fig2 = plt.figure(figsize=(6,6))
        plt.scatter(x=cv_predictions, y=df[response])
        # then, plot the least squares line
        plt.show()

check_rmse(df, 'Appliances', total_list)


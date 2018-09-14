import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as sta
import statsmodels.formula.api as smf
from matplotlib.patches import Ellipse
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import summary_table
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from sklearn.feature_selection import SelectKBest, f_classif, chi2,f_regression
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

## references:
# https://www.ritchieng.com/pandas-scikit-learn/
# https://www.kaggle.com/timolee/a-home-for-pandas-and-sklearn-beginner-how-tos

df = pd.read_csv('P1training_v3.csv', parse_dates=True, index_col=0)
# dependent variables aka response
y = df['Appliances']
# predictors
feature_cols = [col for col in df.columns if 'Appliances' not in col]
x = df[feature_cols]
print(x.head())
print(feature_cols)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

# fit a model
lm = linear_model.LinearRegression()
model = lm.fit(X_train, y_train)
predictions = lm.predict(X_test)
print(y_test - predictions)

#selecting features
selector = SelectKBest(score_func=f_regression, k=5)
fit = selector.fit(df[feature_cols], df['Appliances'])
# Get the raw p-values for each feature, and transform from p-values into scores
scores = -np.log10(selector.pvalues_)
pvalue_dict  = dict(zip(feature_cols, scores))
print(pvalue_dict)
# Plot the scores.
plt.bar(range(len(feature_cols)), scores)
plt.xticks(range(len(feature_cols)), feature_cols, rotation='vertical')
plt.show()
for c, value in enumerate(fit.scores_, 3):
    print(c, value)
features = fit.transform(x)
print(features)
from sklearn.svm import LinearSVR
from sklearn.svm import SVR
estimator = LinearSVR()
rfe = RFE(estimator, 5, step=1)
fit = rfe.fit(x, y)
print("Num Features: {}".format(fit.n_features_))
print("Selected Features: {}".format(fit.support_))
print("Feature Ranking:{}".format(fit.ranking_))
new_dict = dict(zip(feature_cols, fit.support_))
print(new_dict)
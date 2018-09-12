
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as sta
import statsmodels.formula.api as smf
from matplotlib.patches import Ellipse
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (accuracy_score, mean_absolute_error,
                             mean_squared_error, r2_score)
from sklearn.model_selection import KFold, train_test_split
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import summary_table

# reading and loading into dataframe
df = pd.read_csv('P1training.csv')
df['date'] = pd.to_datetime(df['date'])
df['hour'] = pd.to_datetime(df['date']).dt.hour
df['day']= pd.to_datetime(df['date']).dt.dayofweek
df.head()


def forward_selected(data, response):
    """Linear model designed by forward selection.

    Parameters:
    -----------
    data : pandas DataFrame with all possible predictors and response

    response: string, name of response column in data

    Returns:
    --------
    model: an "optimal" fitted statsmodels linear model
           with an intercept
           selected by forward selection
           evaluated by RMSE
    """
    cols = [col for col in df.columns if response not in col]
    cols = [col for col in feature_cols if 'date' not in col]
    print(cols)
    # list to store selected predictors
    selected = []
    # variables to tore score:
    best = 0.0
    current = 0.0

    # split into test train
    kf = KFold(n_splits=10, shuffle=True, random_state=2)
    result = next(kf.split(df), None)
    train = df.iloc[result[0]]
    test = df.iloc[result[1]]
    print(response)
    print(test)
    print(len(test))
    print(test)
    print(len(train))
    # constructure formua
    while cols and current == best:
        for feat in cols:
            print(feat)
            selected.append(feat)
            feature_cols.remove(feat)
            formula = "{0} ~ {1}".format(response, '+'.join(selected))
            model = smf.ols(formula, data=data).fit()
            y_pred = model.predict(test[selected])
            print('RMSE:', np.sqrt(mean_squared_error(y_pred, test['Appliances'])))
            current = np.sqrt(mean_squared_error(y_pred, test['Appliances']))
            print(selected)
            if best:
                if current > best:
                    selected.remove(feat)
                else:
                    best = current
    formula = "{} ~ {}".format(response,
                                   ' + '.join(selected))
    model = smf.ols(formula, data).fit()
    print(model.summary())
    print(model.params)
    return model
# determine predictors
feature_cols = [col for col in df.columns if 'Appliances' not in col]
# dependent variables aka response
y = df['Appliances']
# predictors
x = df[feature_cols]
# split data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)
# statsmodel
#   create fitted model
linear_mod = smf.OLS(y_train, X_train)
linear_res = linear_mod.fit()
#   print coefficients
print(linear_res.params)
#   print summary - OLS regression results
print(linear_res.summary())
# check predictions
predictions = linear_res.predict(X_test)
errors = y_test - predictions
# print(linear_res.conf_int())
# print(linear_res.pvalues)
print('RMSE:', np.sqrt(mean_squared_error(predictions, y_test)))
plt.scatter(y_test, predictions)
plt.xlabel("True Values")
plt.ylabel("Predictions")
# plt.show()

def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:, order]

# need a function to plot the ellipse


def plot_cov_ellipse(cov, pos, nstd=2, ax=None, **kwargs):
    """
    Plots an `nstd` sigma error ellipse based on the specified covariance
    matrix (`cov`). Additional keyword arguments are passed on to the
    ellipse patch artist.

    Parameters
    ----------
        cov : The 2x2 covariance matrix to base the ellipse on
        pos : The location of the center of the ellipse. Expects a 2-element
            sequence of [x0, y0].
        nstd : The radius of the ellipse in numbers of standard deviations.
            Defaults to 2 standard deviations.
        ax : The axis that the ellipse will be plotted on. Defaults to the
            current axis.
        Additional keyword arguments are pass on to the ellipse patch.

    Returns
    -------
        A matplotlib ellipse artist
    """
    if ax is None:
        ax = plt.gca()

    vals, vecs = eigsorted(cov)
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))

    # Width and height are "full" widths, not radius
    width, height = 2 * np.sqrt(nstd) * np.sqrt(vals)
    ellip = Ellipse(xy=pos, width=width, height=height, angle=theta, **kwargs)

    ax.add_artist(ellip)
    return ellip

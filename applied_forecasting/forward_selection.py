
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
#df['day']= pd.to_datetime(df['date']).dt.dayofweek
df.head()

pvalue_threshold = 0.05


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
    counter = cols.copy()
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
    # constructure formua
    for feat in cols:
        selected.append(feat)
        formula = "{0} ~ 1 + {1}".format(response, ' + '.join(selected))
        model = smf.ols(formula, data=train).fit()
        y_pred = model.predict(test[selected])
        print('RMSE:', np.sqrt(
            mean_squared_error(y_pred, test['Appliances'])))
        current = np.sqrt(mean_squared_error(y_pred, test['Appliances']))
        if best == 0.0:
            best = current
            print('best', best)
        if current > best:
            print('current more than best')
            print('currnet', current)
            print('best', best)
            selected.remove(feat)
        else:
            best = current
            pvalues = model.pvalues
            print('pvalues {}\n'.format(pvalues))
            p_dict = pvalues.to_dict()
            for key, value in p_dict.items():
                if value >= pvalue_threshold:
                    print('keys to remove',key)
                    if key == 'Intercept':
                        continue
                    else:
                        print('removing...')
                        selected.remove(key)

    formula = "{} ~ 1+ {}".format(response,
                                  ' + '.join(selected))
    print(formula)
    model = smf.ols(formula, data=train).fit()
    print(model.summary())
    print('\nParams:\n', model.params)
    print('\nPvalues:\n', model.pvalues)
    predictions = model.predict(test[selected])
    print('RMSE:', np.sqrt(
            mean_squared_error(predictions, test[response])))
    return model


# determine predictors
feature_cols = [col for col in df.columns if 'Appliances' not in col]

model = forward_selected(df, 'Appliances')

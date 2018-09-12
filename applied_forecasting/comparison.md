## Feature selection results using scikit learn

    estimator = SVR(kernel="linear")
    rfe = RFE(estimator, 5, step=1)
    fit = rfe.fit(x, y)

Num Features: 5
    
{'lights': False, 'T1': True, 'RH_1': False, 'T2': False, 'RH_2': False, 'T3': True, 'RH_3': False, 'T4': True, 'RH_4': False, 'T5': False, 'RH_5': False, 'T6': False, 'RH_6': False,
'T7': False, 'RH_7': False, 'T8': True, 'RH_8': False, 'T9': True, 'RH_9': False, 'T_out': False, 'Press_mm_hg': False, 'RH_out': False, 'Windspeed': False, 'Visibility': False, 'Tdewpoint': False, 'hour': False}

Feature Ranking:[17  1  3  5  4  1  2  1 12  7 20 10 21  6 13  1 15  1  8 14 19 16 11 22 9 18]

    estimator_2 = LinearSVR()
    selector_2 = RFE(estimator_2, 5, 1)
    selector_2 = selector.fit(X, y)

Num Features: 5

Selected Features: [False False  True False  True  True False False False False False False False False False  True False  True False False False False False False False False]

Feature Ranking:[ 9  3  1  2  1  1 12  8 15 17 22  6 20  4 16  1  5  1 11  7 21 18 10 19 14 13]

{'lights': False, 'T1': False, 'RH_1': True, 'T2': False, 'RH_2': True, 'T3': True, 'RH_3': False, 'T4': False, 'RH_4': False, 'T5': False, 'RH_5': False, 'T6': False, 'RH_6': False, 'T7': False, 'RH_7': False, 'T8': True, 'RH_8': False, 'T9': True, 'RH_9': False, 'T_out': False, 'Press_mm_hg': False, 'RH_out': False, 'Windspeed': False, 'Visibility': False, 'Tdewpoint': False, 'hour': False}

    estimator_3 = LinearRegression()
    selector_3 = RFE(estimator_3, 5, 1)
    selector_3 = selector.fit(X,y) 

Num Features: 5

{'lights': False, 'T1': False, 'RH_1': True, 'T2': True, 'RH_2': True, 'T3': True, 'RH_3': False, 'T4': False, 'RH_4': False, 'T5': False, 'RH_5': False, 'T6': False, 'RH_6': False, 'T7': False, 'RH_7': False, 'T8': False, 'RH_8': False, 'T9': True, 'RH_9': False, 'T_out': False, 'Press_mm_hg': False, 'RH_out': False, 'Windspeed': False, 'Visibility': False, 'Tdewpoint': False, 'hour': False}

Feature Ranking:[ 8  9  1  1  1  1  4  7 16 12 22  5 18 13 11  2  3  1 19  6 20 17 10 21 15 14]


    selector = SelectKBest(score_func=f_regression, k=5)
    fit = selector.fit(df[feature_cols], df[respons])
    # Get the raw p-values for each feature, and transform from p-values into scores
    scores = -np.log10(selector.pvalues_)
    pvalue_dict  = dict(zip(feature_cols, scores))
    print(pvalue_dict)
    # Plot the scores.
    plt.bar(range(len(feature_cols)), scores)
    plt.xticks(range(len(feature_cols)), feature_cols, rotation='vertical')
    plt.show()

{'lights': 125.66487435181583, 'T1': 12.614376551581076, 'RH_1': 25.70312448853656, 'T2': 51.667068316958236, 'RH_2': 13.001073509841417, 'T3': 29.278489694406954, 'RH_3': 5.11527917040632, 'T4': 7.972750022286362, 'RH_4': 1.3242202223458253, 'T5': 2.255571807573618, 'RH_5': 0.32046600008807663, 'T6': 49.828814521581656, 'RH_6': 25.518016386150553, 'T7': 4.0863732492170275, 'RH_7': 11.15981444564585, 'T8': 7.535670466411153, 'RH_8': 29.4447081644904, 'T9': 1.347724787928244, 'RH_9': 9.009151725470517, 'T_out': 36.48758157075807, 'Press_mm_hg': 4.0546376783952125, 'RH_out': 79.46327750890532, 'Windspeed': 24.558129000587765, 'Visibility': 0.25161691650180046, 'Tdewpoint': 1.7669912100853202, 'hour': 154.94091326748614}

## Forward selection using RSME and Pvalue - statsmodel:

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
    
    Appliances ~ 1+ lights + RH_1 + T2 + RH_2 + T3 + T4 + T6 + RH_7 + T8 + RH_8 + T9 + T_out + Windspeed + hour
                            OLS Regression Results
    ==============================================================================
    Dep. Variable:             Appliances   R-squared:                       0.167
    Model:                            OLS   Adj. R-squared:                  0.166
    Method:                 Least Squares   F-statistic:                     189.9
    Date:                Thu, 13 Sep 2018   Prob (F-statistic):               0.00
    Time:                        01:07:44   Log-Likelihood:                -79344.
    No. Observations:               13322   AIC:                         1.587e+05
    Df Residuals:                   13307   BIC:                         1.588e+05
    Df Model:                          14
    Covariance Type:            nonrobust
    ==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept    117.1932     19.045      6.154      0.000      79.863     154.524
    lights         1.8917      0.114     16.650      0.000       1.669       2.114
    RH_1          16.8615      0.650     25.929      0.000      15.587      18.136
    T2           -16.9186      1.311    -12.907      0.000     -19.488     -14.349
    RH_2         -13.5457      0.724    -18.718      0.000     -14.964     -12.127
    T3            25.8014      1.118     23.086      0.000      23.611      27.992
    T4            -3.4667      1.079     -3.214      0.001      -5.581      -1.352
    T6             5.6698      0.670      8.467      0.000       4.357       6.982
    RH_7          -1.0081      0.433     -2.329      0.020      -1.857      -0.160
    T8             6.9669      0.993      7.019      0.000       5.021       8.913
    RH_8          -3.2602      0.400     -8.151      0.000      -4.044      -2.476
    T9           -16.2689      1.554    -10.468      0.000     -19.315     -13.223
    T_out         -5.4024      0.763     -7.076      0.000      -6.899      -3.906
    Windspeed      1.8210      0.383      4.751      0.000       1.070       2.572
    hour           0.9332      0.158      5.910      0.000       0.624       1.243
    ==============================================================================
    Omnibus:                     9253.144   Durbin-Watson:                   0.841
    Prob(Omnibus):                  0.000   Jarque-Bera (JB):           132299.726
    Skew:                           3.252   Prob(JB):                         0.00
    Kurtosis:                      17.001   Cond. No.                     2.22e+03
    ==============================================================================

    Warnings:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
    [2] The condition number is large, 2.22e+03. This might indicate that there are
    strong multicollinearity or other numerical problems.

    Params:
    Intercept    117.193157
    lights         1.891675
    RH_1          16.861496
    T2           -16.918647
    RH_2         -13.545688
    T3            25.801442
    T4            -3.466745
    T6             5.669824
    RH_7          -1.008122
    T8             6.966913
    RH_8          -3.260228
    T9           -16.268909
    T_out         -5.402372
    Windspeed      1.821041
    hour           0.933173
    dtype: float64

    Pvalues:
    Intercept     7.793322e-10
    lights        1.266214e-61
    RH_1         1.186225e-144
    T2            6.904441e-38
    RH_2          3.473349e-77
    T3           1.179356e-115
    T4            1.312795e-03
    T6            2.784411e-17
    RH_7          1.988034e-02
    T8            2.350636e-12
    RH_8          3.938524e-16
    T9            1.520919e-25
    T_out         1.553086e-12
    Windspeed     2.047998e-06
    hour          3.513376e-09
    dtype: float64
    RMSE: 98.0963903453265

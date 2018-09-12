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

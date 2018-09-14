
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
df = pd.read_csv('P1training.csv', parse_dates=True, index_col=0)
df['hour'] = df.index.hour
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
plt.close('all')
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
         # normality check
        residual = y_test - y_pred
        sm.qqplot(residual, stats.distributions.norm, line='r')
        #plt.show()

        print('\nUsing statsmodels:\n')
        formula = "{0} ~ {1}".format(response, '+'.join(cols))
        print(formula)
        model = smf.ols(formula, data=df).fit()
        y_pred = model.predict(X_test[cols])
        print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
        print(model.params)
        print(model.summary())
        print('\nCHECKING RESIDUALS\n')
        residual = y_test - y_pred
        fig, ax = plt.subplots(1,2)
        # axes are in a two-dimensional array, indexed by [row, col]
        ax[0].hist(model.resid_pearson)
        ax[0].set_ylabel('Count')
        ax[0].set_xlabel('Normalized residuals')
        ax[1].scatter(residual, y_pred)

        # normality check
        res = model.resid
        sm.qqplot(res, stats.distributions.norm, line='r')
        #plt.show()

        # linearity check
        ##The Harvey-Collier test performs a t-test (with parameter degrees of freedom) on the recursive residuals.
        ##If the true relationship is not linear but convex or concave the mean of the recursive residuals should differ from 0 significantly.
        import statsmodels.stats.api as sms
        try:
            harvey_collier = sms.linear_harvey_collier(model)
            print(harvey_collier)
        except np.linalg.linalg.LinAlgError as e:
            print(e)

        ## equal variation check
        ### violation of homoscedasticity.
        ### small pvalue = bad
        from statsmodels.stats.diagnostic import het_breuschpagan
        _, pval, __, f_pval = het_breuschpagan(residual, X_test[cols])
        print('Pval', pval)
        print('f_pval', f_pval)

        ## correlation analysis
        # Compute matrix of correlation coefficients
        corr_matrix = np.corrcoef(df[cols].T)
        print(pd.DataFrame(corr_matrix))
        ### https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html
        # Display heat map
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        ax.imshow(corr_matrix)
        ax.set_title('Heatmap of correlation matrix')
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
        # We want to show all ticks...
        ax.set_xticks(np.arange(len(cols)))
        ax.set_yticks(np.arange(len(cols)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(cols)
        ax.set_yticklabels(cols)
        # Loop over data dimensions and create text annotations.
        for i in range(len(cols)):
            for j in range(len(cols)):
                text = ax.text(j, i, round(corr_matrix[i, j], 2),
                       ha="center", va="center", color="black")
        plt.show()


        print("\nCross validation using scikit:\n")
        # check cross validation predictions, 10 splits
        cv_predictions = cross_val_predict(lm, df[cols], df[response], cv=10)
        # check errors
        print('MAE:', mean_absolute_error(df[response], cv_predictions))
        print('RMSE:', np.sqrt(mean_squared_error(df[response], cv_predictions)))
        print('R-Squared:', r2_score(df[response],cv_predictions))
        #print('Score', accuracy_score(df[response], cv_predictions))
        # plot actual vs predicted
        fig3 = plt.figure(figsize=(6,6))
        plt.scatter(x=cv_predictions, y=df[response])
        plt.xlabel('Predictions')
        plt.ylabel('Appliances')
        df['predictions'] = cv_predictions
        # plotting fit results
        fig4, ax = plt.subplots()
        df.Appliances.plot(ax=ax, style='b-')
        # same ax as above since it's automatically added on the right
        df.predictions.plot(ax=ax, style='r-')
        ax.set_xlabel('Predictions')
        ax.set_ylabel('Appliances')
        #print(df.head())
        #df.plot(y=cv_predictions, color='red', linewidth=1)
        #fig4.tight_layout()
        #plt.show()
        print('\nCHECKING RESIDUALS\n')
        residual = df[response] - y_pred
        # axes are in a two-dimensional array, indexed by [row, col]
        fig4 = plt.figure(figsize=(6,6))
        plt.scatter(df.predictions, residual)
        plt.hlines(y = 0, xmin = 0, xmax = 250)
        plt.title('Residual Plot')
        plt.ylabel('Residuals')
        plt.show()


check_rmse(df, 'Appliances', total_list)


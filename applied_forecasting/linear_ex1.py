import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import summary_table
from statsmodels.sandbox.regression.predstd import wls_prediction_std

#read csv into pandas dataframe
data = pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv', index_col=0)
print(data.describe())
# visualize the relationship between the features and the response using scatterplots
# sharey = yes -> shared y-axis
# figsize = size of plot
# nrows=1, ncols=3
fig, axs = plt.subplots(1, 3, sharey=True)
data.plot(kind='scatter', x='TV', y='sales', ax=axs[0], figsize=(16, 8))
data.plot(kind='scatter', x='radio', y='sales', ax=axs[1])
data.plot(kind='scatter', x='newspaper', y='sales', ax=axs[2])
# show plot
# plt.show()

# create a fitted model
lm = smf.ols(formula='sales ~ TV', data=data).fit()
# print the coefficients
print(lm.params)

# 2.2 Making point forecast
# Let's say that there was a new market where the TV advertising spend was $50,000.
# What would we predict for the Sales in that market?
# We can create a dataframe with different values of predictors we are interested in,
#  and use the package to make the point forecast

# create list of values of predictors:
predictor_values = [50, 55, 60, 100, 200]
# create df
new_df = pd.DataFrame({'TV' : predictor_values})
# use the model to make predictions on a new value
print(lm.predict(new_df))

# 2.3 Plotting the linear regression lines
# We can make predictions for the smallest and largest observed values of x,
# and then use the predicted values to plot the least squares line

# create a DataFrame with the minimum and maximum values of TV
TV_max = data['TV'].max()
TV_min = data['TV'].min()
new_df = pd.DataFrame({'TV' : [TV_max, TV_min]})
# make predictions and store them
predictions = lm.predict(new_df)
# plot
data.plot(kind='scatter', x='TV', y='sales')
# then, plot the least squares line
plt.plot(new_df, predictions, c='red', linewidth=2)
# show plt
# plt.show()

# Confidence intervals for the model parameters
# print the confidence intervals (lm.conf_int())
# for the model coefficients
print(lm.conf_int())
# print summary
print(lm.summary())

# Prediction intervals for mean response and response observations
# get the summary results from the linear regression fit
st, sdata, ss2 = summary_table(lm, alpha=0.05)
fittedvalues = sdata[:,2]  # fitted values by the model
predict_mean_se  = sdata[:,3] # standard deviation of the predicted means
predict_mean_ci_low, predict_mean_ci_upp = sdata[:,4:6].T  ## lower and upper limits for the predicted means
predict_ci_low, predict_ci_upp = sdata[:,6:8].T ## lower and upper limits for the predicted observations

## the observation interval can be obtained by builtin function as follows
prstd, predict_ci_low, predict_ci_upp = wls_prediction_std(lm)
## plot the prediction interval
fig, ax = plt.subplots(figsize=(6, 6))
x_pred = data['TV']
idx = np.argsort(x_pred)
ax.scatter(x_pred, data['sales'])
fig.suptitle('Prediction Intervals')
fig.tight_layout(pad=2)
ax.grid(True)
ax.plot(x_pred.iloc[idx], fittedvalues[idx], '-', color='red', linewidth=2)

# interval for observations
ax.fill_between(x_pred.iloc[idx], predict_ci_low[idx], predict_ci_upp[idx], color='#888888', alpha=0.2)
# interval for mean responses
ax.fill_between(x_pred.iloc[idx], predict_mean_ci_low[idx], predict_mean_ci_upp[idx], color='#888888', alpha=0.6)
# plt.show()

# Simulation to demonstrate the uncertainty in estimation
# Here we use simulation to show that when you use different data to estimate the model parameters,
# you can get different results. However, the estimated values follow normal distribution around the true values.
# The uncertainty depends on the sample size, and the scatters of the points.

# simulation settings
n = 100  # sample size of the least square
nrep = 1000 # replication of the simulation
b0 = 1 # intercept of the model
b1 = 2 # slope of the model
sigma = 0.4  # variance of the error terms

## create the array to store the estimated parameters
b0hat = np.zeros(nrep)
b1hat = np.zeros(nrep)

# start the simulation replication
for i in range(nrep):
    # generate samples from the true model
    x = np.random.uniform(0,1,n)
    y = b0+b1*x+np.random.normal(0,sigma, n)
    simdata = pd.DataFrame({'X': x, 'Y': y})
    # create a fitted model
    lm = smf.ols(formula='Y ~ X', data=simdata).fit()
    # obtain the coefficients
    pp = lm.params
    b0hat[i] = pp[0]
    b1hat[i] = pp[1]
# Histogram of the estimated parameters
plt.subplots(1,2, figsize=(12,6))
plt.subplot(121)
plt.hist(b0hat)
plt.title("Histogram of the hat beta0")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.subplot(122)
plt.hist(b1hat)
plt.title("Histogram of the hat beta1")
plt.xlabel("Value")
plt.ylabel("Frequency")
# show plot
plt.show()
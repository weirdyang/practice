import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as sta
import statsmodels.formula.api as smf
from matplotlib.patches import Ellipse
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import summary_table

# read csv into dataframe
df = pd.read_csv('Advertising.csv', index_col=0)
print(df.describe())
print(df.head())

### part 1 individual scatter plots
## single linear regression
def part_one():

    # visualize the relationship between the features and the response using scatterplots
    # sharey = yes -> shared y-axis
    # figsize = size of plot
    # nrows=1, ncols=3
    fig, axs = plt.subplots(nrows=1, ncols=3, sharey=True)
    df.plot(kind='scatter', x='TV', y='sales', ax=axs[0], figsize=(16, 5))
    df.plot(kind='scatter', x='radio', y='sales', ax=axs[1])
    df.plot(kind='scatter', x='newspaper', y='sales', ax=axs[2])
    # show the plot
    plt.show()

    # fit the model
    # https://www.statsmodels.org/stable/example_formulas.html?highlight=ols
    tv_mod = smf.ols(formula='TV~sales', data=df)
    tv_res = tv_mod.fit()
    print(tv_res.params)
    print(tv_res.summary())
    radio_mod = smf.ols(formula='radio~sales', data=df)
    radio_res = radio_mod.fit()
    print(radio_res.params)
    print(radio_res.summary())
    newspaper_mod = smf.ols(formula='newspaper~sales', data=df)
    newspaper_res = newspaper_mod.fit()
    print(newspaper_res.params)
    print(radio_res.summary())

### part 2 multiple linear regression

#   create fitted model
linear_mod = smf.ols('sales ~ TV+radio+newspaper', data=df)
linear_res = linear_mod.fit()
#   print coefficients
print(linear_res.params)
#   print summary - OLS regression results
print(linear_res.summary())
#   get value and covariance of paramter estimate
hat_beta = linear_res.params
cov_beta = linear_res.cov_params()
A = np.matrix(((0,10,0,0), (0,0,1,0)))
#   get the cov of the desired combinated of params
Acov = A * np.mat(cov_beta) * (A.transpose())
Amean = A * (np.mat(hat_beta)).transpose()

def eigsorted(cov):
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        return vals[order], vecs[:,order]

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
    theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))

    # Width and height are "full" widths, not radius
    width, height = 2 * np.sqrt(nstd) * np.sqrt(vals)
    ellip = Ellipse(xy=pos, width=width, height=height, angle=theta, **kwargs)

    ax.add_artist(ellip)
    return ellip

plot_cov_ellipse(Acov, Amean, 2*sta.f.ppf(0.95, 2, 196), color='blue', alpha=0.3)
# plt.axis('tight')
plt.axis((Amean[0]-3*np.sqrt(Acov[0,0]),Amean[0]+3*np.sqrt(Acov[0,0]),Amean[1]-3*np.sqrt(Acov[1,1]),Amean[1]+3*np.sqrt(Acov[1,1])))
plt.xlabel('10b1')
plt.ylabel('b2')
plt.title('95% confidence region for (10b1,b2)')
plt.show()

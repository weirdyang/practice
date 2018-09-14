from __future__ import print_function
from statsmodels.compat import urlopen
import numpy as np
np.set_printoptions(precision=4, suppress=True)
import statsmodels.api as sm
import pandas as pd
pd.set_option("display.width", 100)
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.graphics.api import interaction_plot, abline_plot
from statsmodels.stats.anova import anova_lm

df = pd.read_csv('P1training_v5.csv', parse_dates=True, index_col=0)

plt.figure(figsize=(6,6))
factor_groups = df.groupby(['MAN'])
symbols = ['D', '^', 'o']
colors = ['r', 'g', 'blue']
i = 0
for values, group in factor_groups:
    plt.scatter(group['T1'], group['RH_1'], marker=symbols[i], color=colors[i],
               s=144)
    i += 1
plt.xlabel('T1');
plt.ylabel('Appliances');
plt.show()


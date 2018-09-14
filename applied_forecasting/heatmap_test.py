# Import the necessary
# guide: https://www.datacamp.com/community/tutorials/seaborn-python-tutorial#load
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#load data
posts = pd.read_csv('P1training.csv', encoding='utf-8', parse_dates=True, header='infer', index_col=0)
posts['hour'] = posts.index.hour
posts['weekday'] = posts.index.weekday_name
order = ["Monday","Tuesday","Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
posts['weekday'] = pd.Categorical(posts['weekday'], categories=order, ordered=True)
posts.sort_values(by='weekday', inplace=True)
#print(new_df)
print(posts['hour'])
df = posts.groupby(['hour']).sum()
print(df)

p = pd.pivot_table(posts,  index=['weekday'],
                       values=['Appliances'],
                       aggfunc=np.sum,
                       columns=['hour'],
                       fill_value=0,
                       dropna=False,
                       margins=False)
print(p)
# Initialize figure and ax
#fig, ax = plt.subplots()

#set colour
sns.set_palette(sns.color_palette("GnBu_d"))

# Set the scale of the x-and y-axes
#ax.set(yscale="log")
sns.set_style('darkgrid')
sns.set_context('paper')
#plot points
sns.heatmap(p, annot=False, fmt="g", cmap='BuGn').set_title('When is the best time to post on r/Singapore')
ax2 = plt.axes()
ax2.set_xlabel('Hour of Submission GMT+8')
plt.show()
#sns.heatmap(posts.pivot("hour", "date", "Appliances"), annot=False, cmap="PuBuGn")
#g = sns.factorplot(y='domains', x='counts', kind='bar', data=new_df, palette="BuGn_r")
#g.set_yticklabels(weight='ultralight', linespacing=2)
#plt.suptitle('Top Scoring Domains in r/Singapore')
plt.show()


### code to add labels and hour

df['hour'] = df.index.hour
# initialize all time_of_day to N
df['time_of_day'] = 'N'
# determine indexes for all day time readings
# list to store indexes:
list_of_idx = []
for index, row in df.iterrows():
    if row['hour'] > 8 and row['hour'] < 19:
        list_of_idx.append(index)
# set all labels for day time readingings:
df.loc[list_of_idx, 'time_of_day'] = 'D'

df.to_csv('P1training_v2.csv')

### code eto add labels
df['day_or_night'] = 'D'
list_of_idx = []
for index, row in df.iterrows():
    if row['time_of_day_N'] == 1:
        list_of_idx.append(index)

df.loc[list_of_idx, 'day_or_night'] = 'N'
df.to_csv('P1training_v4.csv')
print(df.head())
#* coding: utf8*
import pygal
import pandas as pd

df = pd.read_csv('kickstart200.tsv', sep='\t', encoding='utf-8')
categories = df.category.unique()
cat_count = df.category.value_counts()
values = list(zip(categories, cat_count))


def barchart():
    bar_chart  = pygal.Bar(legend_at_bottom=True, legend_at_bottom_columns = 4, truncate_legend=-1)
    bar_chart.title = 'Succesful Kickstart Projects grouped by category'
    categories = df.category.unique()
    cat_count = df.category.value_counts()
    values = list(zip(categories, cat_count))
    for item in values:
        if item[1] < 5:
            continue
        bar_chart.add(item[0], item[1])
    bar_chart.render_to_file('barchart.svg')

def scatter():
    xy_chart = pygal.XY(stroke=False, show_legend=False)
    xy_chart.title = "Kickstarter Goal vs Pledged (USD)"
    xy_chart.x_title = "Goal"
    xy_chart.y_title = "Pledged"
    df['usd_goal'] = df['goal'] * df['fx_rate']
    for index, item in df.iterrows():
        xy_chart.add(item['name'], [
            {'value': (item['usd_goal'],  item['pledged']), 'label': item['category'] + " percentage: {}%".format((item['pledged'] / item['usd_goal']) * 100)}])
    xy_chart.render_to_file('scatter.svg')

import pygal
import pandas as pd
import json

input_df = pd.read_csv('index_change.txt', sep='\t', encoding='utf-8')
headers = list(input_df.columns.values)
xy_chart = pygal.XY(legend_at_bottom=True, tooltip_border_radius=10)
xy_chart.title = "Singapore Birth Rates Vs Milk powder prices"
xy_chart.x_title = "Year"
xy_chart.y_title = "% Change. Index: 2004 = 100"
for item in headers:
    if item == 'Year':
        continue
    values = list(zip(input_df['Year'], input_df[item]*100))
    xy_chart.add(item, values)

xy_chart.render_in_browser()

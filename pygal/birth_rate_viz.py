import pygal
import pandas as pd
import json

input_df = pd.read_csv('race_birth_rate.tsv', sep='\t', encoding='utf-8')
headers = list(input_df.columns.values)
xy_chart = pygal.XY(legend_at_bottom=True, tooltip_border_radius=10)
xy_chart.x_labels = (1972, 1975, 1985, 2001, 2016)
xy_chart.title = "Singapore Crude Birth Rates"
xy_chart.x_title = "Year"
xy_chart.y_title = "Crude Birth Rate (per 1000)"
for item in headers:
    if item == 'Year':
        continue
    values = list(zip(input_df['Year'], input_df[item]))
    xy_chart.add(item, values)

xy_chart.render_in_browser()

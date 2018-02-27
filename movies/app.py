import pandas as pd
import json
import pygal
import random
from flask import (Flask, jsonify, render_template, url_for, request)

app = Flask(__name__)
master_df = pd.read_json('static/master.json', orient='records')
jsonfile = open('static/master.json', mode='r', encoding='utf-8')
master_json = json.load(jsonfile)
genre_list = ['Action', 'Drama', 'Comedy', 'Animation', 'All']
kickstart_df = pd.read_csv('static/kickstart200.tsv', sep='\t', encoding='utf-8')


@app.route('/', methods=['GET'])
def index():
    """
    Route that maps to index.html
    """
    search_term = request.args.get("genre")
    print(search_term)
    if (search_term == None) or (search_term=='All'):
        search_term = 'All'
        results = master_df.to_json(orient='records')
    else:
        filtered = master_df[master_df['genre'].str.contains(
            search_term, case=False)]
        results = filtered.to_json(orient='records')
    json_data = json.loads(results)
    xy_chart = pygal.XY(stroke=False, show_legend=False)
    xy_chart.title = "Production Budget vs Worldwide Gross"
    xy_chart.x_title = "Production Budget"
    xy_chart.y_title = "Worldwide Gross"
    for item in json_data:
        xy_chart.add(item['Movie'], [{'value': (item['Production Budget'],  item['Worldwide Gross']) }])
    chart = xy_chart.render_data_uri()
    return render_template('index.html', chart=chart, genres=genre_list, selected_genre=search_term)

@app.route('/ratings', methods=['GET'])
def ratings():
    """
    Route that generates pygal chart
    Attribution: http://biobits.org/bokeh-flask.html
    """
    search_term = request.args.get("genre")
    print(search_term)
    if (search_term is None) or (search_term=='All') :
        search_term = 'All'
        results = master_df.to_json(orient='records')
    else:
        filtered = master_df[master_df['genre'].str.contains(
            search_term, case=False)]
        results = filtered.to_json(orient='records')
    json_data = json.loads(results)
    xy_chart = pygal.XY(stroke=False, show_legend=False)
    xy_chart.title = "Movie's Profit Ratio vs IMDB Rating"
    xy_chart.x_title = "Worldwide Gross to Production Budget Ratio"
    xy_chart.y_title = "IMDB Rating"
    for item in json_data:
        xy_chart.add(item['Movie'], [{'value': ( float(str(item['Ratio'])[:4]),  float(str(item['IMDB'])[:4]))}])
    chart = xy_chart.render_data_uri()
    return render_template('ratings.html', chart=chart, genres=genre_list, selected_genre=search_term)

@app.route('/birthcharts.html', methods=['GET'])
def birth_charts():
    """
    ROute that maps to birth rate comparison charts
    """
    return render_template('birthcharts.html')

@app.route('/ratings_compare/', methods=['GET'])
def comparison():
    """
    Route that generates pygal chart
    Attribution: http://biobits.org/bokeh-flask.html
    """
    search_term = request.args.get("genre")
    print(search_term)
    if (search_term is None) or (search_term=='All') :
        search_term = 'All'
        results = master_df.to_json(orient='records')
    else:
        filtered = master_df[master_df['genre'].str.contains(
            search_term, case=False)]
        results = filtered.to_json(orient='records')
    json_data = json.loads(results)
    xy_chart = pygal.XY(stroke=False, show_legend=False)
    xy_chart.title = "Movie's RT score vs IMDB Rating"
    xy_chart.x_title = "Rotten Tomatoes Score"
    xy_chart.y_title = "IMDB Rating"
    for item in json_data:
        xy_chart.add(item['Movie'], [{'value': (item['RT'],  float(str(item['IMDB'])[:4]))}])
    chart = xy_chart.render_data_uri()
    return render_template('comparison.html', chart=chart, genres=genre_list, selected_genre=search_term)


@app.route('/image', methods=['GET'])
def image():
    """
    """
    random_str = ''.join(random.choices('abcedfg', k=5))
    random_image = 'https://robohash.org/{}'.format(random_str)
    return random_image

@app.route('/kickstarter', methods=['GET'])
def kickstarter():
    """
    routes to kickstarter charts
    """
    cat = kickstart_df.category.unique()
    cat_count = kickstart_df.category.value_counts()
    values = list(zip(cat, cat_count))
    bar_chart  = pygal.Bar(legend_at_bottom=True, legend_at_bottom_columns = 4, truncate_legend=-1)
    bar_chart.title = 'Succesful Kickstart Projects grouped by category'
    for item in values:
        if item[1] < 5:
            continue
        bar_chart.add(item[0], item[1])
    bars = bar_chart.render_data_uri()
    xy_chart = pygal.XY(stroke=False, show_legend=False)
    xy_chart.title = "Kickstarter Goal vs Pledged (USD)"
    xy_chart.x_title = "Goal"
    xy_chart.y_title = "Pledged"
    kickstart_df['usd_goal'] = kickstart_df['goal'] * kickstart_df['fx_rate']
    for index, item in kickstart_df.iterrows():
        percentage = float(str((item['pledged'] / item['usd_goal']) * 100)[:4])
        xy_chart.add(item['name'], [
            {'value': (item['usd_goal'],  item['pledged']), 'label': item['category'] + " Percentage: {}%".format(percentage)}])
    scatter = xy_chart.render_data_uri()
    return render_template('kickstart.html', bars=bars, scatter=scatter)

@app.route('/categories', methods=['GET'])
def categories():
    """
    fiters scatter plot based on dropdown selection
    """
    search_term = request.args.get("category")
    print(search_term)
    cat = kickstart_df.category.unique().tolist()
    cat.append('All')
    if (search_term is None) or (search_term=='All'):
        search_term = 'All'
        results = kickstart_df
    else:
        results = kickstart_df[kickstart_df['category'].str.contains(
            search_term, case=False)]
    xy_chart = pygal.XY(stroke=False, show_legend=False)
    xy_chart.title = "Kickstarter Goal vs Pledged (USD)"
    xy_chart.x_title = "Goal"
    xy_chart.y_title = "Pledged"
    results['usd_goal'] = results['goal'] * results['fx_rate']
    for index, item in results.iterrows():
        percentage = float(str((item['pledged'] / item['usd_goal']) * 100)[:4])
        xy_chart.add(item['name'], [
            {'value': (item['usd_goal'],  item['pledged']), 'label': item['category'] + " Percentage: {}%".format(percentage)}])
    scatter = xy_chart.render_data_uri()
    return render_template('categories.html', categories=cat, selected_category=search_term, chart=scatter)

if __name__ == '__main__':
    app.run(debug=True)


import pandas as pd
from flask import (Flask, jsonify, render_template, url_for)

app = Flask(__name__)
master_df = pd.read_json('static/master.json', orient='records')
print(master_df)


@app.route('/', methods=['GET'])
def index():
    """
    Route that maps to the main index page.
    """
    return render_template('index.html')


@app.route('/generate/<search_term>', methods=['GET'])
def generate(search_term):
    """
    filters df based on genre choice
    """
    print(search_term)
    if search_term == 'all':
        results = master_df.to_json(orient='records')
    else:
        filtered = master_df[master_df['genre'].str.contains(
            search_term, case=False)]
        results = filtered.to_json(orient='records')

    return jsonify(results)

@app.route('/ratings', methods=['GET'])
def ratings():
    """
    Route that maps to ratings page
    """
    return render_template('ratings.html')


if __name__ == '__main__':
    app.run(debug=True)

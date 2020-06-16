import os
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

PARENT_PATH = Path(__file__).parent.resolve()
SAVE_PATH = os.path.join(PARENT_PATH, "solar.csv")


app = dash.Dash(__name__)

def serve_layout():
    df = pd.read_csv(SAVE_PATH)
    return html.Div([
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        editable=True
    ),
    html.Button(id="save-button", n_clicks=0, children="Save"),
    html.Div(id="notification-div", children="Press button to save changes")])


app.layout = serve_layout

@app.callback(
    [Output("data-table", "data"), Output("notification-div", "children")],
    [Input("save-button", "n_clicks")],
    [State("data-table", "data")])
def selected_data_to_csv(nclicks, data):
    if nclicks == 0:
        raise PreventUpdate
    else:
        updated = pd.DataFrame(data)
        updated.to_csv(SAVE_PATH, index=False)
        return updated.to_dict("rows"), f"Data updated and saved to {SAVE_PATH}"


if __name__ == '__main__':
    app.run_server(debug=True)

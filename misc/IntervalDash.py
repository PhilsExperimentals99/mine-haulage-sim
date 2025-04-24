import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(id="live-text"),
    dcc.Interval(id="interval-update", interval=1000, n_intervals=0)  # Updates every 1 sec
])

@app.callback(
    Output("live-text", "children"),
    Input("interval-update", "n_intervals")
)
def update_text(n):
    return f"Interval has fired {n} times!"

if __name__ == '__main__':
    app.run(debug=True)

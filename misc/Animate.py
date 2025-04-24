import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import time


df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "y": [3, 6, 2, 7, 10, 8, 6, 4, 7, 9]
})


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='animated-line-chart'),
    dcc.Interval(id='interval-update', interval=500, n_intervals=0)  # Updates every 500ms
])


@app.callback(
    Output('animated-line-chart', 'figure'),
    Input('interval-update', 'n_intervals')
)
def update_graph(n):
    if n >= len(df):
        n = len(df) - 1  # Avoid exceeding dataset size

    fig = go.Figure()

    # Full line plot
    fig.add_trace(go.Scatter(x=df["x"], y=df["y"], mode="lines", name="Line"))

    # Moving point animation
    fig.add_trace(go.Scatter(x=[df["x"][n]], y=[df["y"][n]], mode="markers",
                             marker=dict(size=10, color="red"),
                             name="Moving Point"))

    # **Fix: Set a fixed y-axis range**
    fig.update_layout(title="Animated Moving Point on Line Chart",
                      xaxis_title="X-axis", yaxis_title="Y-axis",
                      yaxis=dict(range=[df["y"].min() - 1, df["y"].max() + 1])  # Adjust padding if needed
                      )

    return fig


if __name__ == '__main__':
    app.run(debug=True)

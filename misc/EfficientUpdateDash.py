import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Create example dataset with multiple lines
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "y1": [3, 6, 2, 7, 10, 8, 6, 4, 7, 9],  # Animated line
    "y2": [4, 5, 3, 8, 9, 7, 5, 3, 6, 8],  # Static line 1
    "y3": [7, 8, 6, 10, 12, 9, 7, 5, 8, 10]  # Static line 2
})

# Initialize Dash app
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
        n = len(df) - 1  # Prevent exceeding dataset size

    fig = go.Figure()

    # Static lines (always included in updates)
    fig.add_traces([
        go.Scatter(x=df["x"], y=df["y2"], mode="lines", name="Static Line 1"),
        go.Scatter(x=df["x"], y=df["y3"], mode="lines", name="Static Line 2")
    ])

    # Moving point animation on Line 1
    fig.add_trace(go.Scatter(
        x=df["x"], y=df["y1"], mode="lines", name="Animated Line"
    ))
    fig.add_trace(go.Scatter(
        x=[df["x"][n]], y=[df["y1"][n]], mode="markers",
        marker=dict(size=10, color="red"), name="Moving Point"
    ))

    # Set fixed y-axis range & invert y-axis
    fig.update_layout(
        title="Animated Moving Point on Multi-Line Chart",
        xaxis_title="X-axis", yaxis_title="Y-axis",
        yaxis=dict(
            range=[df[["y1", "y2", "y3"]].min().min() - 1,
                   df[["y1", "y2", "y3"]].max().max() + 1],
            autorange="reversed"  # **Inverts the y-axis**
        )
    )

    return fig

# Run Dash server
if __name__ == '__main__':
    app.run(debug=True)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from utils.map import ConstructMapAnnotations, ConstructPointsMap, ConstructRoads, RoadPoints 

# Example data
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y1": [10, 15, 7, 10, 12],
    "y2": [5, 8, 6, 9, 10],
    "y3": [2, 3, 2, 5, 7]
})


roads = ConstructRoads("./data/Roads.csv")
road_points = ConstructPointsMap("./data/RoadPoints.csv")
points_map =  RoadPoints(road_points)
annotations = ConstructMapAnnotations("./data/annotations.csv", road_points)

scatter_data = []
road_coords = {}
for r in roads:
    #print(r)               
    last_point = None
    points = points_map.GetPoints(r.nodes)
    for i, p in enumerate(points):
        if last_point is not None:
            x1 = [last_point.x, p.x]
            y1 = [last_point.y, p.y]
            scatter_data.append(go.Scatter(x=x1, y=y1, mode='lines'))            
            #print(f'p0({last_point.x},{last_point.y}) to p1({p.x}, {p.y}))')
            #plt.axline((last_point.x, last_point.y),(p.x, p.y))
        last_point = p                

    # for a in annotations:
    #     plt.text(a['text_x'], a['text_y'], a['text'], fontsize=8, color='blue')

fig = go.Figure(data=scatter_data,layout=go.Layout(title='Haul Road Map',
                                height=800,  # Set the height to 400 pixels
                                width=1200,   # Set the width to 600 pixels                                
                                xaxis={'title': 'X-Axis'},
                                yaxis={'title': 'Y-Axis'}))

# Invert the y-axis
fig.update_layout(yaxis={'autorange': 'reversed'})

app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Graph(
#         id='multi-line-plot',
#         figure=fig
#     )
# ])

df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "y": [3, 6, 2, 7, 10, 8, 6, 4, 7, 9]
})


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

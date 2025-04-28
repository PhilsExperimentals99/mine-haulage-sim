import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from utils.map import ConstructLocationAssets, ConstructPointsMap, ConstructRoads, RoadPoints 

class MinMaxCoordsFinder:

    def __init__(self):
        self.min_x = float("inf") 
        self.max_x = float("-inf")
        self.min_y = float("inf") 
        self.max_y = float("-inf")

    def Update(self, coords):    
        current_min_y = min(coords['y'])  # Find min of the current list
        self.min_y = min(self.min_y, current_min_y)

        current_max_y = max(coords['y'])  # Find min of the current list
        self.max_y = max(self.max_y, current_max_y)

        current_min_x = min(coords['x'])  # Find min of the current list
        self.min_x = min(self.min_x, current_min_x)

        current_max_x = max(coords['x'])  # Find min of the current list
        self.max_x = max(self.max_x, current_max_x)

    def GetResults(self):
        return self.min_x, self.max_x, self.min_y, self.max_y        


roads = ConstructRoads("./data/Roads.csv")
road_points = ConstructPointsMap("./data/RoadPoints.csv")
points_map =  RoadPoints(road_points)
assets = ConstructLocationAssets("./data/assets.csv", road_points)

scatter_data = []
road_coords = {}
for r in roads:
    #print(r)               
    points = points_map.GetPoints(r.nodes)
    road_name = r.GetUniqueRoadName()
    road_coords[road_name] = {'x' : [], 'y': []}
    for i, p in enumerate(points):         
        road_coords[road_name]['x'].append(p.x)
        road_coords[road_name]['y'].append(p.y)                                    


app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='animated-line-chart'),
    dcc.Interval(id='interval-update', interval=1000, n_intervals=0)  # Updates every 500ms
])

@app.callback(
    Output('animated-line-chart', 'figure'),
    Input('interval-update', 'n_intervals')
)
def update_graph(n):
    fig = go.Figure()    
    selected_coords = road_coords[roads[2].GetUniqueRoadName()]    
    selected_coords_2 = road_coords[roads[7].GetUniqueRoadName()]    
    
    if n >= len(selected_coords['x']):
        n = len(selected_coords['x']) - 1  # Prevent exceeding dataset size

    print(f'Selected Coords = {selected_coords['x']}')        
    print(f'Length Selected Coords = {len(selected_coords['x'])}, n = {n}')        

    minMaxFinder = MinMaxCoordsFinder()
    for r in roads:        
        coords = road_coords[r.GetUniqueRoadName()]
        fig.add_trace(go.Scatter(x=coords["x"], y =coords["y"], mode="lines", name=r.GetUniqueRoadName(), line={'width' : 4}))        
        fig.add_trace(go.Scatter(x=coords["x"], y =coords["y"], mode="markers", name=r.GetUniqueRoadName(), marker=dict(size=4  , color="green")))        
        minMaxFinder.Update(coords)

    # Moving point animation
    fig.add_trace(go.Scatter(x=[selected_coords["x"][n]], y=[selected_coords["y"][n]], mode="markers",
                            marker=dict(size=4  , color="red"),
                            name="Cat 793C-1"))

    fig.add_trace(go.Scatter(x=[selected_coords_2["x"][n]], y=[selected_coords_2["y"][n]], mode="markers",
                            marker=dict(size=4, color="blue"),
                            name="Cat 785C-2"))                

    annotations = []
    for asset in assets:    
        annotations.append(dict(
                x=asset['text_x'],  # Specify the x-coordinate
                y=asset['text_y'],  # Specify the y-coordinate
                text=asset['name'],  # Annotation text
                showarrow=False,  # No arrow
                font=dict(size=8, color="blue"),  # Customize font
                #bgcolor="white",  # Background color
                #bordercolor="black",  # Border color
                #borderwidth=1  # Border width
            )
        )

    fig.update_layout(annotations=annotations)
    map_min_x, map_max_x, map_min_y, map_max_y =  minMaxFinder.GetResults()
    fig.update_layout(
        title="Haul Roads",
        xaxis_title="X-Coords (Metres)",
        yaxis_title="Y-Coords (Metres)",
        yaxis=dict(
            range=[map_min_y - 600, map_max_y + 600],  # Set a fixed y-axis range.Adjust padding if needed
            autorange="reversed"  # reversed y-axis
        ),
        xaxis=dict(
            range=[map_min_x - 300, map_max_x + 300],  # Set a fixed y-axis range.Adjust padding if needed            
        ),
        width=1200,
        height=600
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)

import numpy as np
from matplotlib import pyplot as plt
from utils.map import ConstructLocationAssets, ConstructPointsMap, ConstructRoads, RoadPoints 

def mouse_event(event):
    print('x: {} and y: {}'.format(event.xdata, event.ydata))           

if __name__ == '__main__':

    roads = ConstructRoads("./data/Roads.csv")
    road_points = ConstructPointsMap("./data/RoadPoints.csv")
    points_map =  RoadPoints(road_points)
    assets = ConstructLocationAssets("./data/assets.csv", road_points)

    fig = plt.figure()
    cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
    
    for r in roads:
        #print(r)         
        last_point = None
        points = points_map.GetPoints(r.nodes)
        for i, p in enumerate(points):
            if last_point is not None:
                x1 = [last_point.x, p.x]
                y1 = [last_point.y, p.y]
                plt.plot(x1, y1, color="red", linestyle="--", marker="o", markersize=2)                
                print(f'p0({last_point.x},{last_point.y}) to p1({p.x}, {p.y}))')                
            last_point = p                

    for asset in assets:
        plt.text(asset['text_x'], asset['text_y'], asset['name'], fontsize=8, color='blue')        
        
    # Add labels and legend    
    plt.gca().invert_yaxis()  # Invert the y-axis
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Haul Road Map")
    plt.legend()
    plt.grid()
    plt.show()
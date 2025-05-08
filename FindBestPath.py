import numpy as np
from matplotlib import pyplot as plt
from utils.map import ConstructRoadPointLUT, ConstructRoadNetwork ,RoadNetwork

if __name__ == '__main__':

    road_points_lut = ConstructRoadPointLUT("./data/RouteCoords.cfg")
    road_network = ConstructRoadNetwork("./data/RouteNodes.cfg", road_points_lut)
    # print('Printing road networks.....')
    # print(road_network)

    #start_end_nodes = [(1,10), (225, 200), (225, 5),(215, 200), (215, 216), (94,329), (11,329)]
    #routes = [(1,10),(18,258),(11,34),(34,214),(34,211),(37,329),(329,65),(65,200),(213,216),(87,65),(90,94),(258,215),(215,258)]
    routes = [(1,10),(34,214),(34,211),(37,329)] #,(329,65),(65,200),(213,216),(87,65),(90,94),(258,215),(215,258)]
    nodes_list = []
    for n in routes:
        nodes = road_network.FindMinimumValueRoute(start_id=n[0], target_id=n[1])
        nodes_list.append(nodes)
        print(f'From {n[0]} to {n[1]} nodes={nodes}')
    
    for nodes in nodes_list:        
        last_pt = None
        for node_id in nodes:            
            pt = road_points_lut[node_id]
            if last_pt is not None:
                x_values = [last_pt.x, pt.x]
                y_values = [last_pt.y, pt.y]
                #plt.plot([last_pt.x, last_pt.y], [pt.x, pt.y], 'ro-', label="Original Polyline", markersize=2)
                plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', label="Line Segment", markersize=2)
            plt.annotate(
                str(pt.id),
                xy=(pt.x, pt.y),  # Arrow points at this position
                xytext=(pt.x + 40, pt.y + 60),  # Offset text by dx=10, dy=10
                arrowprops=dict(arrowstyle="->", color="black"),
                fontsize=6,
                color="green"
            )            
            last_pt = pt

    # Add labels and legend    
    plt.gca().invert_yaxis()  # Invert the y-axis
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Haul Road Map")
    plt.grid()
    plt.show()
            
    
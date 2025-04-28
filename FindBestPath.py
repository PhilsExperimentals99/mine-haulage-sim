import numpy as np
from matplotlib import pyplot as plt
from utils.map import ConstructRoadPointLUT, ConstructRoadNetwork ,RoadNetwork

if __name__ == '__main__':

    road_points_lut = ConstructRoadPointLUT("./data/RouteCoords.cfg")
    road_network = ConstructRoadNetwork("./data/RouteNodes.cfg", road_points_lut)
    # print('Printing road networks.....')
    # print(road_network)

    start_end_nodes = [(1,10), (225, 200), (225, 5),(215, 200), (215, 216)]
    for n in start_end_nodes:
        nodes = road_network.FindMinimumValueRoute(start_id=n[0], target_id=n[1])
        print(f'From {n[0]} to {n[1]} nodes={nodes}')
    
    
    #road_network.AddSegment()
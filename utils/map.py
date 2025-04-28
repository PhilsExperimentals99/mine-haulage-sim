import ast
import heapq
import numpy as np

class Road:
    def __init__(self, start, end, nodes):
        self.start = start
        self.end = end
        self.nodes = nodes
        self.unique_name = self.start + ' <--> ' + self.end 

    def GetUniqueRoadName(self):
        return self.unique_name        

    def __str__(self):
        return f'From {self.start} to {self.end} with {len(self.nodes)} via points'  

class RoadPoint:
    def __init__(self, id ,x, y, point_type, annotation):
        self.x = x
        self.y = y
        self.id = id
        self.type = point_type
        self.annotation = annotation

    def __str__(self):
        return f'Road point {self.id} of type {self.type} at ({self.x}, {self.y})'            

class RoadPoints:
    def __init__(self, points_table):
        self.points_lut = points_table
        
    def __str__(self):
        return f'{len(self.points_lut.keys)} #points in road map'

    def GetPoints(self, node_indices_list):
        print(f'node_indices_list = {node_indices_list}')
        return [self.points_lut[p] for p in node_indices_list]
    
    def GetPoint(self, point_id):
        point = self.points_lut[point_id]
        return point
    

class RoadNetwork:
    def __init__(self):
        self.graph = {}

    def __str__(self):
        return "\n".join(f"{key}: {value}" for key, value in self.graph.items())        

    def AddSegment(self, start_label, end_label,  segment_cost):
        """ 
        start_label - label associated with a node (x,y) that starts the route segment 
        end_label - label associated with a node (x,y) that ends the route segment
        metric_value - value of a metric of the segment that is used to find optimal path
        """
        if start_label not in self.graph:
            self.graph[start_label] = []
        self.graph[start_label].append((end_label, segment_cost))

    def FindMinimumValueRoute(self, start_id, target_id):
        """ 
        Finds optimal path using Dijkstra's to minimise cumulative path_value.   
        Cycles prevention when searching graph is used 
        """
        pq = [(0, start_id)]  # Priority queue with (cost, node)
        segment_costs = {node: float('inf') for node in self.graph}
        segment_costs[start_id] = 0
        previous_nodes = {}
        visited = set()  # Track processed nodes

        while pq:
            current_seg_cost, current_node = heapq.heappop(pq)

            if current_node in visited:
                continue  # Skip re-processing completed nodes
            
            visited.add(current_node)

            if current_node == target_id:
                break

            for neighbor, cost in self.graph.get(current_node, []):                 
                total_cost = current_seg_cost + cost
                if total_cost < segment_costs[neighbor]:
                    segment_costs[neighbor] = total_cost
                    heapq.heappush(pq, (total_cost, neighbor))
                    previous_nodes[neighbor] = current_node

        path = []
        node = target_id
        while node in previous_nodes:
            path.insert(0, node)
            node = previous_nodes[node]
        if path:
            path.insert(0, start_id)

        return path if path else None


def ConstructRoads(filename):
    roads = []
    with open(filename, "r") as file:
        for line in file:                    
            #print(line)
            fields = line.split(":")  
            start_name = fields[0].strip(' ')
            if start_name.startswith('#'):
                continue
            nodes_str = fields[2].strip(' ')
            nodes_str = nodes_str.strip('\n')
            nodes = ast.literal_eval(nodes_str)            
            end_name = fields[1].strip(' ')
            roads.append(Road(start_name, end_name, nodes))        
    return roads    


def ConstructPointsMap(filename):
    scale_to_metres = 1 #3.75
    road_points = {}
    with open(filename, "r") as file:
        for line in file:
            if len(line) > 5:
                fields = line.split(",")                
                print(fields)
                id_str = fields[0].strip(' ')
                if id_str.startswith('#'):
                    continue                
                id = int(id_str)                
                x = float(fields[1].strip(' ').strip('\n')) * scale_to_metres
                y = float(fields[2].strip(' ').strip('\n')) * scale_to_metres
                if len(fields) <= 3:
                    point_type = 'U'
                    description = 'Undefined'
                else:
                    point_type = fields[3].strip(' ')
                    description = fields[4].strip(' ').strip('\n')
                road_points[id] = RoadPoint(id,x,y,point_type,description)
    return road_points  

def ConstructLocationAssets(filename, road_points):
    assets = []
    with open(filename, "r") as file:
        for line in file:
            if len(line) > 1:
                fields = line.split(",")
                print(fields)
                id_str = fields[0].strip(' ')
                if id_str.startswith('#'):
                    continue
                point_id = int(id_str)    
                offset_x = float(fields[1].strip(' '))
                offset_y = float(fields[2].strip(' '))
                road_point = road_points[point_id]
                text_x = road_point.x + offset_x
                text_y = road_point.y + offset_y
                text = road_point.annotation
                assets.append({'name': text, 'text_x' : text_x, 'text_y' : text_y, 'x' : road_point.x, 'y' : road_point.y, 'point_id' : point_id})
    return assets


def ConstructRoads(filename):
    roads = []
    with open(filename, "r") as file:
        for line in file:                    
            #print(line)
            fields = line.split(":")  
            start_name = fields[0].strip(' ')
            if start_name.startswith('#'):
                continue
            nodes_str = fields[2].strip(' ')
            nodes_str = nodes_str.strip('\n')
            nodes = ast.literal_eval(nodes_str)            
            end_name = fields[1].strip(' ')
            roads.append(Road(start_name, end_name, nodes))        
    return roads

def ConstructRoadPointLUT(filename):
    scale_to_metres = 1 #3.75
    road_points = {}
    with open(filename, "r") as file:
        for line in file:
            if len(line) > 5:  # a heuristic to differentiate a blank line
                fields = line.split(",")                
                #print(fields)
                id_str = fields[0].strip(' ')
                if id_str.startswith('#'):
                    continue                
                id = int(id_str)                
                x = float(fields[1].strip(' ').strip('\n')) * scale_to_metres
                y = float(fields[2].strip(' ').strip('\n')) * scale_to_metres
                if len(fields) <= 3:
                    point_type = 'U'
                    description = 'Undefined'
                else:
                    point_type = fields[3].strip(' ')
                    description = fields[4].strip(' ').strip('\n')
                road_points[id] = RoadPoint(id,x,y,point_type,description)
    return road_points  



def ConstructRoadNetwork(filename, road_point_lut):
    road_net = RoadNetwork()
    with open(filename, "r") as file:
        for line in file:                    
            #print(line)
            fields = line.split(":")  
            start_id_str = fields[0].strip(' ')            
            if start_id_str.startswith('#'):
                continue
            start_id = int(start_id_str)
            nodes_str = fields[1].strip(' ')
            nodes_str = nodes_str.strip('\n')
            nodes = ast.literal_eval(nodes_str)            
            start_point = road_point_lut[start_id]
            #print(f'start node {start_id} with ({start_point.x}, {start_point.y}) to nodes {nodes}')
            for next_id in nodes:    
                end_point = road_point_lut[next_id]
                distance = euclidean_distance(np.array([start_point.x, start_point.y]), np.array([end_point.x, end_point.y]))                                
                road_net.AddSegment(start_id, next_id, distance)
    return road_net                

def euclidean_distance(point1, point2):
    """Calculates Euclidean distance between two points."""
    return np.linalg.norm(np.array(point1) - np.array(point2))

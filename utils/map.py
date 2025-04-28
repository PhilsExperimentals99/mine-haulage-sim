import ast
import heapq
import math

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


class RoadNetwork:
    def __init__(self, constant_multiplier=1):
        self.graph = {}
        self.constant_multiplier = constant_multiplier

    def add_segment(self, start_label, end_label, max_speed, gradient, start_coords, end_coords):
        """ Adds a directed road segment with expected travel duration """
        distance = math.dist(start_coords, end_coords)  # Compute real-world distance
        duration = gradient * self.constant_multiplier * (distance / max_speed)  # Compute travel duration

        if start_label not in self.graph:
            self.graph[start_label] = []
        self.graph[start_label].append((end_label, duration))

    def dijkstra(self, start_label, target_label):
        """ Finds shortest path using Dijkstra's algorithm with cycle prevention """
        pq = [(0, start_label)]  # Priority queue with (cost, node)
        durations = {node: float('inf') for node in self.graph}
        durations[start_label] = 0
        previous_nodes = {}
        visited = set()  # Track processed nodes

        while pq:
            current_duration, current_node = heapq.heappop(pq)

            if current_node in visited:
                continue  # Skip re-processing completed nodes
            
            visited.add(current_node)

            if current_node == target_label:
                break

            for neighbor, duration in self.graph.get(current_node, []):
                total_duration = current_duration + duration
                if total_duration < durations[neighbor]:
                    durations[neighbor] = total_duration
                    heapq.heappush(pq, (total_duration, neighbor))
                    previous_nodes[neighbor] = current_node

        path = []
        node = target_label
        while node in previous_nodes:
            path.insert(0, node)
            node = previous_nodes[node]
        if path:
            path.insert(0, start_label)

        return path if path else None

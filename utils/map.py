import ast

class Road:
    def __init__(self, start, end, nodes):
        self.start = start
        self.end = end
        self.nodes = nodes

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
    scale_to_metres = 3.75
    road_points = {}
    with open(filename, "r") as file:
        for line in file:
            if len(line) > 5:
                fields = line.split(",")
                print(fields)
                id_str = fields[0].strip(' ')
                # if isinstance(id_str, str):
                #     continue                
                id = int(id_str)                
                x = float(fields[1].strip(' ')) * scale_to_metres
                y = float(fields[2].strip(' ')) * scale_to_metres
                point_type = fields[3].strip(' ')
                description = fields[4].strip(' ').strip('\n')
                road_points[id] = RoadPoint(id,x,y,point_type,description)
    return road_points  

def ConstructMapAnnotations(filename, road_points):
    annotations = []
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
                annotations.append({'text': text, 'text_x' : text_x, 'text_y' : text_y, 'x' : road_point.x, 'y' : road_point.y})
    return annotations

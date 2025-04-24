import numpy as np
import ast
from matplotlib import pyplot as plt
 
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
            nodes_str = fields[2].strip(' ')
            nodes_str = nodes_str.strip('\n')
            nodes = ast.literal_eval(nodes_str)
            start_name = fields[0].strip(' ')
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
                id = int(fields[0].strip(' '))
                x = float(fields[1].strip(' ')) * scale_to_metres
                y = float(fields[2].strip(' ')) * scale_to_metres
                point_type = fields[3].strip(' ')
                description = fields[4].strip(' ').strip('\n')
                road_points[id] = RoadPoint(id,x,y,point_type,description)
    return road_points  

def ConstructAnnotations(filename, road_points):
    annotations = []
    with open(filename, "r") as file:
        for line in file:
            if len(line) > 1:
                fields = line.split(",")
                print(fields)
                point_id = int(fields[0].strip(' '))    
                offset_x = float(fields[1].strip(' '))
                offset_y = float(fields[2].strip(' '))
                road_point = road_points[point_id]
                text_x = road_point.x + offset_x
                text_y = road_point.y + offset_y
                text = road_point.annotation
                annotations.append({'text': text, 'text_x' : text_x, 'text_y' : text_y, 'x' : road_point.x, 'y' : road_point.y})
    return annotations

def mouse_event(event):
    print('x: {} and y: {}'.format(event.xdata, event.ydata))           

if __name__ == '__main__':

    fig = plt.figure()
    cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
    
    roads = ConstructRoads("./data/Roads.csv")
    road_points = ConstructPointsMap("./data/RoadPoints.csv")
    points_map =  RoadPoints(road_points)

    annotations = ConstructAnnotations("./data/annotations.csv", road_points)

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
                #plt.axline((last_point.x, last_point.y),(p.x, p.y))
            last_point = p                

    for a in annotations:
        plt.text(a['text_x'], a['text_y'], a['text'], fontsize=8, color='blue')
        # plt.annotate(a['text'], xy=(a['x'], a['y']), xytext=(a['text_x'], a['text_y']),
        #     arrowprops=dict(facecolor='black', shrink=0.01))
        
    # Add labels and legend    
    plt.gca().invert_yaxis()  # Invert the y-axis
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Haul Road Map")
    plt.legend()
    plt.grid()

    plt.show()
import numpy as np
import matplotlib.pyplot as plt
from utils.map import ConstructLocationAssets, ConstructPointsMap, ConstructRoads, RoadPoints, euclidean_distance 

# Define adjustable merging threshold
MERGE_DISTANCE_THRESHOLD = 10  # You can change this value

def merge_close_points_0(points, threshold=MERGE_DISTANCE_THRESHOLD):
    """Merges points that are closer than the given threshold."""
    merged_points = []
    
    while points:
        base_point = points.pop(0)
        close_points = [base_point]

        points_to_keep = []
        for pt in points:
            if euclidean_distance(base_point, pt) < threshold:
                close_points.append(pt)
            else:
                points_to_keep.append(pt)

        points = points_to_keep

        # Compute average position for merged points
        avg_x = np.mean([p[0] for p in close_points])
        avg_y = np.mean([p[1] for p in close_points])
        merged_points.append([avg_x, avg_y])

    return np.array(merged_points)

def merge_close_points(orig_points, threshold=MERGE_DISTANCE_THRESHOLD):
    """Merges points that are closer than the given threshold."""
    
    merged_points = []
    if isinstance(orig_points, np.ndarray):
        points = orig_points.tolist()
    else:
        points = orig_points.copy()
        
    base_point = points.pop(0)
    close_points = [base_point]
    while points:        
        next_point = points.pop(0)        
        if euclidean_distance(base_point, next_point) < threshold:                        
            close_points.append(next_point)
        else:
            if len(close_points) > 1:  # at least 2 close enough points
                # Compute average position for merged points
                avg_x = np.mean([p[0] for p in close_points])
                avg_y = np.mean([p[1] for p in close_points])
                merged_points.append([avg_x, avg_y])                
            else:                                
                merged_points.append(base_point)
            close_points = [base_point]
        base_point = next_point # check distance from the next point
        

    return np.array(merged_points)

def offset_polyline(points, offset_distance):
    """Offsets polyline points to create parallel roads."""
    offset_points = []
    n = len(points)

    for i in range(n - 1):
        dx = points[i+1, 0] - points[i, 0]
        dy = points[i+1, 1] - points[i, 1]

        if dx == 0:  # Special case: vertical segment
            nx, ny = np.sign(dy), 0  # Normal purely horizontal
        else:
            norm_factor = np.sqrt(dx**2 + dy**2)
            nx, ny = -dy / norm_factor, dx / norm_factor
        
        # Offset both points along the normal direction
        offset_p1 = points[i] + offset_distance * np.array([nx, ny])
        offset_p2 = points[i+1] + offset_distance * np.array([nx, ny])

        offset_points.append(offset_p1)
        offset_points.append(offset_p2)

    return np.array(offset_points)
    #return offset_points

# Load road data
roads = ConstructRoads("./data/Roads.csv")
road_points = ConstructPointsMap("./data/RoadPoints.csv")
points_map = RoadPoints(road_points)
assets = ConstructLocationAssets("./data/assets.csv", road_points)
road_points_sanitized = ConstructPointsMap("./data/RouteCoords.cfg")
#road_map_sanitized = RoadPoints(road_points_sanitized)

offset_point_list = []
for r in roads:
    points=[]
    map_points = points_map.GetPoints(r.nodes)    
    for i, p in enumerate(map_points):
        points.append([p.x, p.y])

    # Merge close points before storing
    #merged_points = merge_close_points(points)


    offset_point_list.append(np.array(points))        

offset_distance = 10

original_points_count = 1  # Initialize marker count, red = 1, blue = 200
offset_points_count = 200

SHOW_LOADED_ROUTES = False
SHOW_EMPTY_ROUTES = False
SHOW_LOADED_POINTS_LABEL = True
SHOW_LOADED_POINTS_LABEL = True
SHOW_ORIG_POINTS_LABEL = False 
SHOW_OFFSET_POINTS_LABEL = False
SHOW_SANITIZED_POINTS = True

for points in offset_point_list:
    offset_pts = offset_polyline(points, offset_distance)
    #merged_points = np.array(merge_close_points((offset_pts))) #(offset_pts)
    
    # Plot original and offset polylines
    plt.plot(points[:, 0], points[:, 1], 'ro-', label="Original Polyline", markersize=2)
    plt.plot(offset_pts[:, 0], offset_pts[:, 1], 'bo-', label="Offset Polyline", markersize=2)
    
    # Place annotation near the start point of each line
    #start_x, start_y = points[0]  # Get start point coordinates
    if SHOW_ORIG_POINTS_LABEL:
        for pt in points:
            start_x, start_y = pt
            # print(pt)
            plt.annotate(
                str(original_points_count),
                xy=(start_x, start_y),  # Arrow points at this position
                xytext=(start_x + 10, start_y + 10),  # Offset text by dx=10, dy=10
                arrowprops=dict(arrowstyle="->", color="black"),
                fontsize=12,
                color="red"                
            )
            original_points_count += 1  # Increment marker count
        
    if SHOW_OFFSET_POINTS_LABEL:        
        for pt in offset_pts:
            start_x, start_y = pt
            #print(pt)
            plt.annotate(
                str(offset_points_count),
                xy=(start_x, start_y),  # Arrow points at this position
                xytext=(start_x + 40, start_y + 60),  # Offset text by dx=10, dy=10
                arrowprops=dict(arrowstyle="->", color="black"),
                fontsize=10,
                color="blue"
            )
            offset_points_count += 1  # Increment marker count        

if SHOW_SANITIZED_POINTS:
    for pt in road_points_sanitized.values():
        print(pt)
        plt.annotate(
            str(pt.id),
            xy=(pt.x, pt.y),  # Arrow points at this position
            xytext=(pt.x + 40, pt.y + 60),  # Offset text by dx=10, dy=10
            arrowprops=dict(arrowstyle="->", color="black"),
            fontsize=6,
            color="green"
        )
        plt.plot(pt.x, pt.y, 'D', markersize=3, color='cyan')

# Add labels and legend    
plt.gca().invert_yaxis()  # Invert the y-axis
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Haul Road Map")
plt.grid()
plt.show()

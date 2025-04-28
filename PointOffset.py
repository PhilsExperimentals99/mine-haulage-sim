import numpy as np
import matplotlib.pyplot as plt
from utils.map import ConstructLocationAssets, ConstructPointsMap, ConstructRoads, RoadPoints 

def offset_polyline(points, offset_distance):
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

# Example polyline (includes vertical segment)
#points = np.array([[0, 0], [2, 3], [2, 7], [5, 7], [7, 4]])

roads = ConstructRoads("./data/Roads.csv")
road_points = ConstructPointsMap("./data/RoadPoints.csv")
points_map =  RoadPoints(road_points)
assets = ConstructLocationAssets("./data/assets.csv", road_points)

offset_point_list = []
for r in roads:
    points=[]
    map_points = points_map.GetPoints(r.nodes)    
    for i, p in enumerate(map_points):
        points.append([p.x, p.y])
    offset_point_list.append(np.array(points))        

#points = np.array(points)

offset_distance = 10

# for points in offset_point_list:
#     offset_pts = offset_polyline(points, offset_distance)
#     # Plot original and offset polyline
#     plt.plot(points[:, 0], points[:, 1], 'ro-', label="Original Polyline")
#     plt.plot(offset_pts[:, 0], offset_pts[:, 1], 'bo-', label="Offset Polyline")

count = 1  # Initialize marker count

for points in offset_point_list:
    offset_pts = offset_polyline(points, offset_distance)

    # Plot original and offset polylines
    plt.plot(points[:, 0], points[:, 1], 'ro-', label="Original Polyline")
    plt.plot(offset_pts[:, 0], offset_pts[:, 1], 'bo-', label="Offset Polyline")

    # Place annotation near the start point of each line
    start_x, start_y = points[0]  # Get start point coordinates
    plt.annotate(
        str(count),
        xy=(start_x, start_y),  # Point where arrow points
        xytext=(start_x + 50, start_y + 50),  # Offset position for text
        arrowprops=dict(arrowstyle="->", color="black"),
        fontsize=12,
        color="black"
    )

    count += 1  # Increment marker count

# Add labels and legend    
plt.gca().invert_yaxis()  # Invert the y-axis
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Haul Road Map")
#plt.legend()
plt.grid()
plt.show()

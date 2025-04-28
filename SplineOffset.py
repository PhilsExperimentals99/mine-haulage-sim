import numpy as np
from scipy.interpolate import splev, splprep
import matplotlib.pyplot as plt
from utils.map import ConstructLocationAssets, ConstructPointsMap, ConstructRoads, RoadPoints 

def compute_offset_spline(points, offset_dist):
    # Fit a B-spline curve through given points
    tck, u = splprep(points.T, s=0)

    # Compute derivatives to get tangent vectors
    dx, dy = splev(u, tck, der=1)
    
    # Compute normal vectors (perpendicular to tangent)
    norms = np.sqrt(dx**2 + dy**2)
    nx, ny = -dy / norms, dx / norms  # Rotate tangent to get normals
    
    # Offset points along normal direction
    offset_x = points[:,0] + offset_dist * nx
    offset_y = points[:,1] + offset_dist * ny
    offset_points = np.array([offset_x, offset_y])
    
    return offset_points, tck

# Example control points
#control_points = np.array([[0, 0], [1, 2], [3, 3], [4, 1], [5, 0]])
control_points = []

roads = ConstructRoads("./data/Roads.csv")
road_points = ConstructPointsMap("./data/RoadPoints.csv")
points_map =  RoadPoints(road_points)
assets = ConstructLocationAssets("./data/assets.csv", road_points)

r = roads[0]
points = points_map.GetPoints(r.nodes)
for i, p in enumerate(points):
    control_points.append([p.x, p.y])

control_points = np.array(control_points)

print(control_points)

def mouse_event(event):
    print('x: {} and y: {}'.format(event.xdata, event.ydata))           

fig = plt.figure()
cid = fig.canvas.mpl_connect('button_press_event', mouse_event)

# Compute offset spline
offset_distance = 10 #0.5
offset_spline, _ = compute_offset_spline(control_points, offset_distance)

# Plot original and offset spline
plt.plot(control_points[:,0], control_points[:,1], 'ro-', label="Original B-Spline")
plt.plot(offset_spline[0], offset_spline[1], 'bo-', label="Offset B-Spline")
# plt.legend()
# plt.show()

# Add labels and legend    
plt.gca().invert_yaxis()  # Invert the y-axis
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Haul Road Map")
plt.legend()
plt.grid()
plt.show()

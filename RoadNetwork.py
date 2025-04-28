

import heapq
class RoadNetwork:
    def __init__(self):
        self.graph = {}

    def add_segment(self, start, end, cost):
        """ Adds a directed road segment to the network """
        if start not in self.graph:
            self.graph[start] = []
        self.graph[start].append((end, cost))

    def dijkstra(self, start, target):
        """ Finds shortest path using Dijkstra's algorithm """
        pq = [(0, start)]  # Priority queue with (cost, node)
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        previous_nodes = {}

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node == target:
                break

            for neighbor, cost in self.graph.get(current_node, []):
                distance = current_distance + cost
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
                    previous_nodes[neighbor] = current_node

        path = []
        node = target
        while node in previous_nodes:
            path.insert(0, node)
            node = previous_nodes[node]
        if path:
            path.insert(0, start)

        return path if path else None

# Example: Creating a mine road network with dual carriageway segments
road_network = RoadNetwork()
road_network.add_segment((0,0), (1,0), 1)  # Forward carriageway
road_network.add_segment((1,0), (2,0), 1)
road_network.add_segment((2,0), (3,0), 1)

road_network.add_segment((3,0), (2,0), 1)  # Return carriageway
road_network.add_segment((2,0), (1,0), 1)
road_network.add_segment((1,0), (0,0), 1)

# Adding intersection connections for left-hand drive
road_network.add_segment((1,0), (1,-1), 0.5)  # Left turn
road_network.add_segment((1,-1), (2,-1), 1)
road_network.add_segment((2,-1), (2,0), 0.5)  # Rejoining

# Finding shortest path between two points
start_point = (0,0)
end_point = (3,0)
shortest_path = road_network.dijkstra(start_point, end_point)
print("Shortest Path:", shortest_path)

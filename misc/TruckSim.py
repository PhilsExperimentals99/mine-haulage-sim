import simpy
import math

class HaulTruck:
    def __init__(self, env, name, distance, v_max, acceleration, deceleration):
        self.env = env
        self.name = name
        self.distance = distance  # Total road distance in meters
        self.v_max = v_max  # Max speed in m/s
        self.acceleration = acceleration  # Acceleration in m/s^2
        self.deceleration = deceleration  # Deceleration in m/s^2
        self.process = env.process(self.run())

    def compute_travel_time(self):
        # Compute time to reach max speed
        t_accel = self.v_max / self.acceleration
        d_accel = 0.5 * self.acceleration * (t_accel ** 2)

        # Compute time to decelerate
        t_decel = self.v_max / self.deceleration
        d_decel = 0.5 * self.deceleration * (t_decel ** 2)

        # Compute time at constant speed
        d_cruise = self.distance - (d_accel + d_decel)
        if d_cruise > 0:
            t_cruise = d_cruise / self.v_max
        else:
            t_cruise = 0  # If distance is short, it might only accelerate/decelerate

        total_time = t_accel + t_cruise + t_decel
        return total_time

    def run(self):
        while True:
            print(f"{self.name} starts traveling at {self.env.now}")
            travel_time = self.compute_travel_time()
            print(f'travel_time = {travel_time}')
            yield self.env.timeout(travel_time)
            print(f"{self.name} completes travel at {self.env.now}")

# Create simulation environment
env = simpy.Environment()

# Example truck parameters
truck = HaulTruck(env, "Truck-1", distance=500, v_max=15, acceleration=1.5, deceleration=1.2)

# Run simulation for a sufficient time
env.run(until=100)

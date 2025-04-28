import simpy
import random

class Car:
    def __init__(self, env, car_id, speed, interval, intersection_dist, braking_dist, road):
        self.env = env
        self.car_id = car_id
        self.speed = speed  # Initial speed (m/s)
        self.interval = interval  # Sampling interval (seconds)
        self.position = 0  # Distance traveled
        self.intersection_dist = intersection_dist  # Distance to intersection
        self.braking_dist = braking_dist  # Distance at which braking starts
        self.road = road  # Reference to shared road object
        self.brake_event = env.event()  # Event to trigger braking
        env.process(self.drive())

    def drive(self):
        while self.position < self.intersection_dist:
            # Check distance from car ahead
            ahead_car = self.road.get_car_in_front(self)
            if ahead_car and (ahead_car.position - self.position < 5):  # Maintain safe distance
                print(f"Time {self.env.now}: Car {self.car_id} slowing down to avoid {ahead_car.car_id}")
                self.speed = max(self.speed - 2, 1)  # Reduce speed but don't stop

            # Move car based on speed and interval
            self.position += self.speed * self.interval
            print(f"Time {self.env.now}: Car {self.car_id} at {self.position:.2f}m, Speed {self.speed:.2f} m/s")

            # Check if braking needs to start
            if self.position >= self.intersection_dist - self.braking_dist:
                print(f"Time {self.env.now}: Car {self.car_id} triggering braking event!")
                self.brake_event.succeed()  # Trigger event
                yield from self.brake()  # Start braking process
                yield from self.intersection_logic()  # Handle intersection
                return  # Stop normal driving after braking

            yield self.env.timeout(self.interval)  # Wait for next update

    def brake(self):
        while self.speed > 0:
            self.speed -= 2  # Reduce speed by 2 m/s every interval
            if self.speed < 0:
                self.speed = 0
            self.position += self.speed * self.interval
            print(f"Time {self.env.now}: Car {self.car_id} braking at {self.position:.2f}m, Speed {self.speed:.2f} m/s")
            yield self.env.timeout(self.interval)  # Wait for next update
        
        print(f"Time {self.env.now}: Car {self.car_id} stopped at {self.position:.2f}m!")

    def intersection_logic(self):
        print(f"Time {self.env.now}: Car {self.car_id} waiting for right-of-way...")
        while self.road.check_cross_traffic():
            yield self.env.timeout(1)  # Wait if cross traffic is present
        print(f"Time {self.env.now}: Car {self.car_id} proceeds through the intersection!")

class Road:
    def __init__(self, env, num_cars):
        self.env = env
        self.cars = []
        self.create_cars(num_cars)

    def create_cars(self, num_cars):
        for i in range(num_cars):
            speed = random.randint(8, 12)  # Randomized speed
            car = Car(self.env, i+1, speed, interval=1, intersection_dist=50, braking_dist=10, road=self)
            self.cars.append(car)

    def get_car_in_front(self, car):
        # Get the car immediately ahead (sorted by position)
        ahead_cars = [c for c in self.cars if c.position > car.position]
        return min(ahead_cars, key=lambda c: c.position, default=None)

    def check_cross_traffic(self):
        # Simulate presence of cross traffic at intersection randomly
        return random.choice([True, False])

# Simulation parameters
SIM_DURATION = 40  # Max simulation time (seconds)
env = simpy.Environment()

# Initialize road with multiple cars
road = Road(env, num_cars=3)

# Run simulation
env.run(until=SIM_DURATION)

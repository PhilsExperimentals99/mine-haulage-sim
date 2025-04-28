import simpy
import random

class Car:
    def __init__(self, env, car_id, speed, interval, intersection_dist, braking_dist, road, lane=1):
        self.env = env
        self.car_id = car_id
        self.speed = speed  # Initial speed (m/s)
        self.interval = interval  # Sampling interval (seconds)
        self.position = 0  # Distance traveled
        self.intersection_dist = intersection_dist  # Distance to intersection
        self.braking_dist = braking_dist  # Distance at which braking starts
        self.road = road  # Reference to shared road object
        self.brake_event = env.event()  # Event to trigger braking
        self.lane = lane  # Current lane (1 = main, 2 = overtaking)
        env.process(self.drive())

    def drive(self):
        while self.position < self.intersection_dist:
            # Check for the car in front in the same lane
            ahead_car = self.road.get_car_in_front(self)
            if ahead_car and (ahead_car.position - self.position < 5):  # Maintain safe distance
                if self.road.can_overtake(self):  # Check if overtaking is possible
                    print(f"Time {self.env.now}: Car {self.car_id} overtaking {ahead_car.car_id}")
                    self.lane = 2  # Move to overtaking lane
                else:
                    print(f"Time {self.env.now}: Car {self.car_id} slowing down for {ahead_car.car_id}")
                    self.speed = max(self.speed - 2, 1)  # Reduce speed but don't stop

            # Move car based on speed and interval
            self.position += self.speed * self.interval
            print(f"Time {self.env.now}: Car {self.car_id} at {self.position:.2f}m, Speed {self.speed:.2f} m/s, Lane {self.lane}")

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
        self.lane = 1  # Reset lane after passing intersection

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
        # Get the car immediately ahead in the same lane
        ahead_cars = [c for c in self.cars if c.position > car.position and c.lane == car.lane]
        return min(ahead_cars, key=lambda c: c.position, default=None)

    def can_overtake(self, car):
        # Check if the overtaking lane is clear
        return all(c.position < car.position - 5 or c.position > car.position + 5 for c in self.cars if c.lane == 2)

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

# run continously
import simpy
import random

def run_simulation():
    env = simpy.Environment()
    road = Road(env, num_cars=3)

    try:
        env.run()  # Runs indefinitely until manually stopped
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

# Call this function to start the simulation
run_simulation()


# external stop
import simpy

def car_process(env, brake_event):
    print(f"Time {env.now}: Car is moving...")
    yield brake_event  # Wait until event is triggered externally
    print(f"Time {env.now}: Car starts braking!")

def external_trigger(env, brake_event, trigger_time):
    yield env.timeout(trigger_time)  # Wait for external condition
    print(f"Time {env.now}: External trigger activates braking!")
    brake_event.succeed()  # Manually trigger the event

env = simpy.Environment()
brake_event = env.event()

env.process(car_process(env, brake_event))
env.process(external_trigger(env, brake_event, trigger_time=5))

env.run()

#externally stooping car sims

import simpy
import random

class Car:
    def __init__(self, env, car_id, speed, interval, intersection_dist, braking_dist, road, stop_event, lane=1):
        self.env = env
        self.car_id = car_id
        self.speed = speed  # Initial speed (m/s)
        self.interval = interval  # Sampling interval (seconds)
        self.position = 0  # Distance traveled
        self.intersection_dist = intersection_dist  # Distance to intersection
        self.braking_dist = braking_dist  # Distance at which braking starts
        self.road = road  # Reference to shared road object
        self.stop_event = stop_event  # Global stop event
        self.brake_event = env.event()  # Event to trigger braking
        self.lane = lane  # Current lane (1 = main, 2 = overtaking)
        env.process(self.drive())

    def drive(self):
        while self.position < self.intersection_dist:
            # Periodically check if stop_event has been triggered
            if self.stop_event.triggered:
                print(f"Time {self.env.now}: Car {self.car_id} stopping due to global stop!")
                return  # Exit process immediately

            # Check for the car in front in the same lane
            ahead_car = self.road.get_car_in_front(self)
            if ahead_car and (ahead_car.position - self.position < 5):  # Maintain safe distance
                if self.road.can_overtake(self):  # Check if overtaking is possible
                    print(f"Time {self.env.now}: Car {self.car_id} overtaking {ahead_car.car_id}")
                    self.lane = 2  # Move to overtaking lane
                else:
                    print(f"Time {self.env.now}: Car {self.car_id} slowing down for {ahead_car.car_id}")
                    self.speed = max(self.speed - 2, 1)  # Reduce speed but don't stop

            # Move car based on speed and interval
            self.position += self.speed * self.interval
            print(f"Time {self.env.now}: Car {self.car_id} at {self.position:.2f}m, Speed {self.speed:.2f} m/s, Lane {self.lane}")

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
            # Check if stop_event is triggered before continuing
            if self.stop_event.triggered:
                print(f"Time {self.env.now}: Car {self.car_id} stopping due to global stop!")
                return

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
        self.lane = 1  # Reset lane after passing intersection

class Road:
    def __init__(self, env, num_cars, stop_event):
        self.env = env
        self.cars = []
        self.stop_event = stop_event  # Global stop event
        self.create_cars(num_cars)

    def create_cars(self, num_cars):
        for i in range(num_cars):
            speed = random.randint(8, 12)  # Randomized speed
            car = Car(self.env, i+1, speed, interval=1, intersection_dist=50, braking_dist=10, road=self, stop_event=self.stop_event)
            self.cars.append(car)

    def get_car_in_front(self, car):
        # Get the car immediately ahead in the same lane
        ahead_cars = [c for c in self.cars if c.position > car.position and c.lane == car.lane]
        return min(ahead_cars, key=lambda c: c.position, default=None)

    def can_overtake(self, car):
        # Check if the overtaking lane is clear
        return all(c.position < car.position - 5 or c.position > car.position + 5 for c in self.cars if c.lane == 2)

    def check_cross_traffic(self):
        # Simulate presence of cross traffic at intersection randomly
        return random.choice([True, False])

def external_stop(env, stop_event, stop_time):
    yield env.timeout(stop_time)  # Wait until stop condition is met
    print(f"\nTime {env.now}: External stop event triggered! Stopping simulation...\n")
    stop_event.succeed()  # Manually trigger stop event

# Simulation setup
env = simpy.Environment()
stop_event = env.event()  # Create global stop event
road = Road(env, num_cars=3, stop_event=stop_event)

env.process(external_stop(env, stop_event, stop_time=20))  # Stop simulation at time 20
env.run()



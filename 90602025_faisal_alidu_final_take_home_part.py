# -*- coding: utf-8 -*-
"""90602025_Faisal Alidu_Final_Take_Home_part.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12SxgisfT1x9lfYi5V4DVNCFFSBuU4kwb

### **Simulation of Autonomous Vehicles for Urban Mobility (Summer 2024)**

`Scenario Description:`

The goal is to optimize traffic flow and reduce congestion at a busy urban intersection by integrating autonomous vehicles (AVs) into the existing traffic system. The simulation will compare the performance of a mixed traffic environment (AVs and human-driven vehicles) with a scenario where only conventional vehicles are present.

**Begin Simulation**
"""

from google.colab import drive
drive.mount('/content/drive')

!apt-get update

!apt-get install -y sumo sumo-tools sumo-doc

!pip install traci

!pip install --upgrade traci

import traci

import sumolib

!pip install tensorflow opencv-python

from google.colab import files
uploaded = files.upload()

# Path to the SUMO binary
sumoBinary = "sumo"
sumoCmd = [sumoBinary, "-c", "/content/simulation.sumocfg"]

traci.start(sumoCmd)

step = 0
while step < 1000:
    traci.simulationStep()
    vehicle_ids = traci.vehicle.getIDList()

    for vehicle_id in vehicle_ids:
        # Get the current speed of the vehicle
        speed = traci.vehicle.getSpeed(vehicle_id)

        # Get the vehicle's position
        position = traci.vehicle.getPosition(vehicle_id)

        # Get the vehicle in front of the current vehicle (if any)
        leader_vehicle = traci.vehicle.getLeader(vehicle_id)

        if leader_vehicle is not None:
            leader_id, gap = leader_vehicle

            # Decision logic for adaptive cruise control
            safe_gap = 5.0  # Safe following distance in meters
            if gap < safe_gap:
                # Slow down to maintain a safe distance
                new_speed = max(speed - 1.0, 0)  # Reduce speed by 1 m/s, but not below 0
                traci.vehicle.slowDown(vehicle_id, new_speed, 1000)  # Apply slowdown over 1 second
            else:
                # Maintain or increase speed slightly if safe
                new_speed = min(speed + 1.0, traci.vehicle.getMaxSpeed(vehicle_id))
                traci.vehicle.slowDown(vehicle_id, new_speed, 1000)

        # Decision logic for lane changing
        current_lane = traci.vehicle.getLaneID(vehicle_id)
        if traci.vehicle.getTypeID(vehicle_id) == "autonomous" and traci.lane.getLastStepOccupancy(current_lane) < 0.5:
            # Try to change lanes if the current lane is congested
            possible_lanes = traci.vehicle.getLaneChangePossibleLanes(vehicle_id)
            for lane in possible_lanes:
                if traci.lane.getLastStepOccupancy(lane) < 0.5:
                    traci.vehicle.changeLane(vehicle_id, lane, 1000)
                    break

    step += 1

traci.close()

average_speed = sum(traci.vehicle.getSpeed(veh) for veh in vehicle_ids) / len(vehicle_ids)
print(f"Average speed of vehicles: {average_speed}")

import matplotlib.pyplot as plt

plt.plot( average_speed)
plt.title("Average Vehicle Speed Over Time")
plt.xlabel("Time Step")
plt.ylabel("Average Speed (m/s)")
plt.show()
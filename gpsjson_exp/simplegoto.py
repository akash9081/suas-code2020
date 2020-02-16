#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.
Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import math

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default(lat=38.145206, lon=-76.428473)
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

import json
with open('new_gps.json') as p:
        data2 = json.load(p)
corr=data2["waypoints"]
a=[]
for i in corr:
    a.append([i["latitude"],i["longitude"],i["altitude"]])

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5



def distance_to_current_waypoint(targetWaypointLocation):
    """
    Gets distance in metres to the current waypoint. 
    It returns None for the first waypoint (Home location).
    """
    #if nextwaypoint==0:
    #   return None
    #missionitem=vehicle.commands[nextwaypoint-1] #commands are zero indexed
    #lat = missionitem.x
    #lon = missionitem.y
    #alt = missionitem.z
    #targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(5)

print("Set default/target airspeed to 3")
vehicle.airspeed = 1

#print("Going towards first point for 30 seconds ...")
#point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
#vehicle.simple_goto(point1)

# sleep so we can see the change in map
#time.sleep(30)

#print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
#point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
#vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
#time.sleep(30)

for ji in range(len(a)):
    print('Going towards ',ji,' point for 30 seconds ...')
    point = LocationGlobalRelative(a[ji][0],a[ji][1],a[ji][2])
    vehicle.simple_goto(point)
    print(distance_to_current_waypoint(point))
    while(distance_to_current_waypoint(point)>=0.5):
        print('hello')
        print("distance to current way point is : ",distance_to_current_waypoint(point))
        time.sleep(1)
    print('yahan pe rukega ye 3 sec ke lie')
    time.sleep(3)
    print('3 sec pure hue')
    print(point)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()


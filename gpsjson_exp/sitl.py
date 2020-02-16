import dronekit_sitl
from time import sleep

"""
runs dronekit which is necessary for connecting to the Mission planner simulator. 
"""

if __name__ == '__main__':
    sitl = dronekit_sitl.start_default(lat=29.867295, lon = 77.898946)
    print("Connection String:", sitl.connection_string())

    try:
        while True:
            sleep(1)
    except:
        sitl.stop()

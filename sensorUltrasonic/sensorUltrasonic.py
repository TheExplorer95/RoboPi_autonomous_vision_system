from gpiozero import DistanceSensor
from time import sleep
from sys import quit

# Setting HC-SR04 range [0.02 m, 4 m]
max_distance = 4
min_distance = 0.02

# Initializing the PINS for the sensors
echo_sensor_side_left =
trigger_sensor_side_left =

echo_sensor_side_right =
trigger_sensor_side_right =

echo_sensor_back_left =
trigger_sensor_back_left =

echo_sensor_back_right =
trigger_sensor_back_right =

# Initializing the sensor variables
sensor_side_left = DistanceSensor(echo=echo_sensor_side_left,
                                    trigger=trigger_sensor_side_left,
                                    max_distance=max_distance,
                                    threshold_distance=min_distance)
sensor_side_right = DistanceSensor(echo=echo_sensor_side_right,
                                    trigger=trigger_sensor_side_right,
                                    max_distance=max_distance,
                                    threshold_distance=min_distance)
sensor_back_left = DistanceSensor(echo=echo_sensor_back_left,
                                    trigger=trigger_sensor_back_left,
                                    max_distance=max_distance,
                                    threshold_distance=min_distance)
sensor_back_right = DistanceSensor(echo=echo_sensor_back_right,
                                    trigger=trigger_sensor_back_right,
                                    max_distance=max_distance,
                                    threshold_distance=min_distance)

def main():
    try:
        while True:
            print('HR-SR04 distances:')
            print(f'Side left - {sensor_side_left.distance} m')
            print(f'Side right - {sensor_side_right.distance} m')
            print(f'Back left - {sensor_back_left.distance} m')
            print(f'Back right - {sensor_back_right.distance} m')
    except KeyboardInterrupt:
        quit()

if __name__ == '__main__':
    main()

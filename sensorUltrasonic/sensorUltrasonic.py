from gpiozero import DistanceSensor
from time import sleep

class UltrasonicSensors:
    # Setting HC-SR04 range [0.02 m, 4 m]
    max_distance = 4
    min_distance = 0.02

    def __init__(self, **kwargs):
        # Initializing the PINS for the sensors
        echo_sensor_side_left = 19
        trigger_sensor_side_left = 13

        echo_sensor_side_right = 6
        trigger_sensor_side_right = 5

        echo_sensor_back_left = 22
        trigger_sensor_back_left = 27

        echo_sensor_back_right = 17
        trigger_sensor_back_right = 4

        if len(kwargs) > 0:
            for key, value in kwargs.items():
                key = value

            print('[INFO] - Changes made to default Ultrasonic setup')

        # Initializing the sensor variables
        self.sensor_side_left = DistanceSensor(echo=echo_sensor_side_left,
                                    trigger=trigger_sensor_side_left,
                                    max_distance=self.max_distance,
                                    threshold_distance=self.min_distance)
        self.sensor_side_right = DistanceSensor(echo=echo_sensor_side_right,
                                    trigger=trigger_sensor_side_right,
                                    max_distance=self.max_distance,
                                    threshold_distance=self.min_distance)
        self.sensor_back_left = DistanceSensor(echo=echo_sensor_back_left,
                                    trigger=trigger_sensor_back_left,
                                    max_distance=self.max_distance,
                                    threshold_distance=self.min_distance)
        self.sensor_back_right = DistanceSensor(echo=echo_sensor_back_right,
                                    trigger=trigger_sensor_back_right,
                                    max_distance=self.max_distance,
                                    threshold_distance=self.min_distance)

if __name__ == '__main__':
    try:
        while True:
            sleep(2)
            print('HR-SR04 distances:')
            print(f'Side left - {sensor_side_left.distance} m')
            print(f'Side right - {sensor_side_right.distance} m')
            print(f'Back left - {sensor_back_left.distance} m')
            print(f'Back right - {sensor_back_right.distance} m')
    except KeyboardInterrupt:
        quit()

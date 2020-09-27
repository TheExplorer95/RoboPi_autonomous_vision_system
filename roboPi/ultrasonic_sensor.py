from gpiozero import DistanceSensor
from time import sleep
from threading import Thread

class UltrasonicSensors:
    # Setting HC-SR04 range [0.02 m, 4 m]
    max_distance = 4
    min_distance = 0.02

    def __init__(self):
        # PINS for the sensors
        self.echo_sensor_side_left = 19
        self.trigger_sensor_side_left = 13
        self.echo_sensor_side_right = 6
        self.trigger_sensor_side_right = 5
        self.echo_sensor_back_left = 22
        self.trigger_sensor_back_left = 27
        self.echo_sensor_back_right = 17
        self.trigger_sensor_back_right = 4

        self.readings = tuple()         # left, right, back left, back right
      
        self.init_sensors()        
        self.init_reading()

    def init_sensors(self):
        # Initializing the sensor variables
        self.sensor_side_left = DistanceSensor(echo=self.echo_sensor_side_left,
                                    trigger=self.trigger_sensor_side_left,
                                    max_distance=self.max_distance,
                                    threshold_distance=self.min_distance)
        self.sensor_side_right = DistanceSensor(echo=self.echo_sensor_side_right,
                                    trigger=self.trigger_sensor_side_right,
                                    max_distance=self.max_distance,
                                    threshold_distance=self.min_distance)
        self.sensor_back_left = DistanceSensor(echo=self.echo_sensor_back_left,
                                    trigger=self.trigger_sensor_back_left,
                                    max_distance=self.max_distance,
                                    threshold_distance=self.min_distance)
        self.sensor_back_right = DistanceSensor(echo=self.echo_sensor_back_right,
                                    trigger=self.trigger_sensor_back_right,
                                    max_distance=self.max_distance,
                                    threshold_distance=self.min_distance)
    
    def init_reading(self):
        def init_reading_thread():
            while True:
                try:
                    self.readings = (self.sensor_side_left.distance, 
                            self.sensor_side_right.distance,
                            self.sensor_back_left.distance,
                            self.sensor_back_right.distance)
                    sleep(1)
                except Exception:
                    pass
        self.read_sensor_thread = Thread(target=init_reading_thread, args=())
        self.read_sensor_thread.daemon = True
        self.read_sensor_thread.start()

    def getReading(self):
        return self.readings

if __name__ == '__main__':
    US = UltrasonicSensors()
    while True:
        sleep(2)
        for v in US.getReading():
            print(v)

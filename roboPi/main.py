from threading import Thread
import drive_controler 
import ultrasonic_sensor
import stereo_cam
import realsense_cam

if __name__=='__main__':
    DC = drive_controler.DriveControler()
    US = ultrasonic_sensor.UltrasonicSensors()
    CAM = stereo_cam.CamThread(ID=0, name='frontCam', showVideo=True)
    RS = realsense_cam.RealCam(showVideo=True)

    while True:
        sleep(1)
        print(US.getReading())

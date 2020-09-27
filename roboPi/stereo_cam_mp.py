import numpy as np
import cv2 as cv
from multiprocessing import Process
from threading import Thread
import logging
from collections import deque
from time import sleep

class CamThread():
    
    def __init__(self, ID: int, name: str, deque_size=3):
        
        # set camera properties
        self.camID = ID
        self.name = name
        
        # Flag to check if camera is valid/working
        self.online = False
        self.frames = deque(maxlen=deque_size)
        
        # initialize cam and check if working
        self.init_stream()
        sleep(0.1)
        self.init_frame_grabbing() 

    def init_stream(self):    
        def init_stream_thread():
            try:
                self.cam = cv.VideoCapture(self.camID)
                if not self.cam.isOpened() and not self.online:
                    raise Exception(f'{self.name} was not initialized.') 
                elif self.cam.isOpened() and not self.online:
                    print(f'{self.name} was initialized')
                    logging.info(f'{self.name} was initialized')
                    self.online = True
                    self.cam.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('J', 'P', 'E', 'G'))
            except Exception as e:
                logging.exception(str(e))

        self.loadStreamThread = Process(target=init_stream_thread, args=())
        self.loadStreamThread.daemon = True
        self.loadStreamThread.start()

    def init_frame_grabbing(self):
        def get_frame():
            try:
                while True:
                    if self.online:
                        ret, frame = self.cam.read()
                        if ret:
                            self.frames.append(frame) 
                        #else:    
                        #    raise Exception(f'Camera stream {self.name} is broken')      
            except Exception as e:
                logging.exception(str(e))
            finally:
                self.end()

        self.grabFrameThread = Thread(target=get_frame, args=())
        self.grabFrameThread.daemon = True
        self.grabFrameThread.start()
    
    def frame_available(self):
        return len(self.frames) > 0

    def get_frame(self):
        if len(self.frames) == 0:
            raise Exception('[Error] - You did not check if frames are available')
        return self.frames.pop()

    def show_video(self):
        try:    
            while True:
                if self.frame_available():
                    loadedFrame = self.get_frame()
                    cv.namedWindow(self.name, cv.WINDOW_AUTOSIZE)
                    cv.imshow(self.name, loadedFrame)
                    cv.waitKey(1)
        except Exception as e:
            print(str(e))
            quit()

    def end(self):
        self.cam.release()
        cv.destroyAllWindows()
        logging.info(f'"{self.name}" was shut down.')

class StereoCam():    

    def __init__(self, leftCam: int, rightCam: int):
        self.leftCam = CamThread(leftCam, 'left Camera')
        self.rightCam = CamThread(rightCam, 'right Camera')
        sleep(1)

    def show_video(self, name='StereoView'):
        try:    
            cv.namedWindow(name, cv.WINDOW_AUTOSIZE)
            if self.leftCam.frame_available() and self.rightCam.frame_available():    
                concat = np.hstack((self.leftCam.get_frame(), self.rightCam.get_frame()))
                cv.imshow(name, concat)
                cv.waitKey(1)
        except Excception as e:
            print(str(e))
            quit()

if __name__ == '__main__':
    state = 'single'

    if state=='single':
        cam0 = CamThread(0, 'leftCam')
#        cam1 = CamThread(6, 'rightCam')
        sleep(1)
        cam0.show_video()
#        cam1.show_video()
    if state=='stereo':
        cam = StereoCam(7, 6)
        cam.show_video()


else:
    # creating sub root error logger
    subLogger = SubLogger(name='roboPi.stereoCam')

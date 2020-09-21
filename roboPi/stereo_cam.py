import numpy as np
import cv2 as cv
import threading
import logging
from utils.loggingUtils import SubLogger

LOCK = threading.RLock()

class CamThread(threading.Thread):
    
    def __init__(self, ID, name):
        threading.Thread.__init__(self)
        self._camID = int(ID)
        self._name = name
        self.frame = None
        self.ret = None
        
        # initialize cam and check if working
        try:
            self._cam = cv.VideoCapture(self._camID)
            if not self._cam.isOpened():
                logging.error(f'{self._name} was not initialized.') 
            else:
                logging.info(f'{self._name} was initialized')
        except Exception as e:
            logging.exception(str(e))

    def run(self):
    # thread for image acquesition thats run when passing .start()
        while True:
            #with LOCK:
            self.ret, self.frame = self._cam.read()
            if not self.ret:
                logging.error(f'Stream is broken')      
                break
        
        return None

    def end(self):
        self._cam.release()
        cv.destroyAllWindows()
        logging.info(f'"{self._name}" was shut down.')

        return None

class StereoCams():    

    def __init__(self, leftCam, rightCam):
        self._leftCam = CamThread(leftCam, 'left Camera')
        self._rightCam = CamThread(rightCam, 'right Camera')
        cv.waitKey(200)
        self._leftCam.start()
        self._rightCam.start()
        cv.waitKey(200)

    def show_video(self, name='StereoView'):
        cv.namedWindow(name, cv.WINDOW_AUTOSIZE)
        pic =np.hstack((self._leftCam.frame, self._rightCam.frame))
        print(pic, pic.shape)
        if self._leftCam.ret and self._rightCam.ret:
            cv.imshow(name, pic)
        #cv.imshow(name, np.hstack((self._leftCam.frame, self._rightCam.frame)))
            cv.waitKey(1)
        else:
            cv.imshow(name, self._leftCam.frame)
            cv.waitKey(1)
        return None
        
    def shutDown(self):
        self._leftCam.end()
        self._rightCam.end()

        return None

if __name__ == '__main__':
    from utils.loggingUtils import MainLogger
    logger = MainLogger()
 
    myStereo = StereoCams(6, 7)
    try:
        while True:
            myStereo.show_video()
    except Exception as e:
        logging.exception(str(e))
    finally:
        myStereo.shutDown()
else:
    # creating sub root error logger
    subLogger = SubLogger(name='roboPi.stereoCam')

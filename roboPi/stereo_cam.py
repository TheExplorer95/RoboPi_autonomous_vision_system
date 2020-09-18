import numpy as np
import cv2 as cv
import threading
import concurrent.futures
from .. import loggingUtils

LOCK = threading.Rlock()

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
            if not cam.isOpened():
                logging.error(f'{self._name} was not initialized.') 
            else:
                logging.info(f'{self._name} was initialized')
        except Exception as e:
            logging.exception(str(e))

    def run(self):
    # thread for image acquesition thats run when passing .start()
        while True:
            with LOCK:
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

    def show_video(self, name='StereoView'):
        cv.namedWindow(name, cv.WINDOW_AUTOSIZE)
        cv.imshow(name, np.hstack((self._leftCam.frame, self._rightCam.frame)))
        keyCode = cv.waitKey(1)

        return None
        
    def shutDown():
        self._leftCam.end()
        self._rightCam.end()

        return None

if __name__ == '__main__':
    from ..utils.loggingUtils import mainLogger

    logger = MainLogger()

    myStereo = StereoCams(6, 7)
    try:
        while True:
            StereoCams.show_video()
    except Exception as e:
        logging.exception(str(e))
    finally:
        StereoCams.shutDown()
else:
    # creating sub root error logger
    subLogger = SubLogger(name='root.stereoCam')

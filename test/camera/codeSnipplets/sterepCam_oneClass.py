import numpy as np
import cv2 as cv
import threading
import concurrent.futures
''' Implementation of threading for cameras which does not work'''

class StereoCams(threading.Thread):

    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self._lock = threading.Lock()
        self.frame0 = None
        self.frame1 = None
        self._amountCams = 2

        # standart cam input
        self._kwargs = {'cam0': '/dev/video4', 'cam1': '/dev/video5', 'preview': False}

        # process kwargs
        _keys = {'cam0', 'cam1', 'preview'}
        self._kwargs.update((k, v) for k, v in kwargs.items() if k in
                _keys) 

        # lock devices
        self._cap = list()        
        
        print('befpre', self._amountCams)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._amountCams) as ex:
            futures = []
            for dev in range(self._amountCams):
                futures.append(ex.submit(self.lock_dev, dev))
            while True:
                if all(concurrent.futures.as_completed(futures)):
                    break

        print('after')
        #self._cap0 = cv.VideoCapture(self.__dict__['cam0'])
        #self._cap1 = cv.VideoCapture(self.__dict__['cam1']) 

        # detect if connection was establish sucessfully
        if not self._cap[0].isOpened() or not self._cap[1].isOpened():
            raise ValueError('[ERROR] Cannot open camera stream.')
     
    def lock_dev(self, dev):
        print(f'init dev{dev}')
        self._cap.append(cv.VideoCapture(self._kwargs['cam'+str(dev)]))
        print(f'finished to init dev{dev}')
    
    def capture(self):
        ret0, self.frame0 = self._cap0.read()
        ret1, self.frame1 = self._cap1.read()
        
        # detect if stream is broken
        if not ret0 or not ret1:
            raise ValueError('[Error] - Stereo stream is broken')

        return None

    def show_video(self, name='StereoView'):
        cv.namedWindow(name, cv.WINDOW_AUTOSIZE)
        cv.imshow(name, np.hstack((self.frame0, self.frame1)))
        keyCode = cv.waitKey(1)

        return None
        
    def end(self):
        self._cap0.release()
        self._cap1.release()
        cv.destroyAllWindows()
        print('[Info] - Stereocams shutted down.')

        return None

if __name__ == '__main__':
    SV = StereoCams()
    try:
        SV.capture()
        SV.show_video()
    finally:
        SV.end()

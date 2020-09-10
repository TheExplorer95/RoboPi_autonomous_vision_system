import numpy as np
import cv2 as cv

class StereoCams:

    def __init__(self, **kwargs):
        self.frame0 = None
        self.frame1 = None

        # standart cam input
        self._cameras = {cam0: '/dev/video0', cam1: '/dev/video1'}

        # process kwargs
        allowed_keys = {'cam0', 'cam1'}
        self._cameras.update((k, v) for k, v in kwargs.items() if k in
                allowed_Keys) 

        # lock devices
        self._cap0 = cv.VideoCapture(cam0)
        self._cap1 = cv.VideoCapture(cam1)
    
        # detect if connection was establish sucessfully
        if not cap0.isOpened() or not cap1.isOpened():
            raise ValueError('[ERROR] Cannot open camera stream.')
               
    def capture():
        ret0, self.frame0 = self._cap0.read()
        ret1, self.frame1 = self._cap1.read()
        
        # detect if stream is broken
        if not ret0 or not ret1:
            raise ValueError('[Error] - Stereo stream is broken')

        return None

    def show_video(name='StereoView'):
        cv.namedWindow(name, cv.WINDOW_AUTOSIZE)
        cv.imshow(name, np.hstack((self.frame0, self.frame1)))
        keyCode = cv.waitKey(1)

        return None
        
    def end():
        self._cap0.release()
        self._cap1.release()
        cv.destroyAllWindows()
        print('[Info] - Stereocams shutted down.')

        return None



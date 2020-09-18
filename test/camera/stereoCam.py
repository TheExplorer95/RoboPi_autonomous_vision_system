import numpy as np
import cv2 as cv

class StereoCams:

    def __init__(self, **kwargs):
        self.frame0 = None
        self.frame1 = None

        # standart cam input
        self._cameras = {'cam0': '/dev/video4', 'cam1': '/dev/video5'}

        # process kwargs
        allowed_keys = {'cam0', 'cam1'}
        self._cameras.update((k, v) for k, v in kwargs.items() if k in
                allowed_Keys) 

        # lock devices
        self._cap0 = cv.VideoCapture(self._cameras['cam0'])
        self._cap1 = cv.VideoCapture(self._cameras['cam1'])
    
        # detect if connection was establish sucessfully
        if not self._cap0.isOpened() or not self._cap1.isOpened():
            raise ValueError('[ERROR] Cannot open camera stream.')
               
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

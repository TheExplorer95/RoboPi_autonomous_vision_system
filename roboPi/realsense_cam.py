import pyrealsense2 as rs
import numpy as np
import cv2 as cv

class RealCam:

    def __init__(self, depth=True, color=True, pixel=(640, 480), frames=30):
        # initialization of camera
        self._pipeline = rs.pipeline()
        self._config = rs.config()
        self.frame = None
        self.imageDepth = None
        self.imageColor = None
        self.depthColormap = None

        if depth:
            self._config.enable_stream(rs.stream.depth, 
                    pixel[0],
                    pixel[1], 
                    rs.format.z16, 
                    frames)
        if color:
            self._config.enable_stream(rs.stream.color, 
                    pixel[0], 
                    pixel[1],
                    rs.format.bgr8, 
                    frames)
        
        self._pipeline.start(self._config)

    def capture(self):
        self.frame = self._pipeline.wait_for_frames()
        frameDepth = self.frame.get_depth_frame()
        frameColor = self.frame.get_color_frame()

        if not frameDepth or not frameColor:
            raise ValueError('[Error] - Realsense stream is broken.')

        self.imageDepth = np.asarray(frameDepth.get_data())
        self.imageColor = np.asarray(frameColor.get_data())
            
        self.depthColormap = cv.applyColorMap(cv.convertScaleAbs(self.imageDepth,
            alpha=0.03), cv.COLORMAP_JET)
        
        return None

    def show_video(self,name='Realsense'):
        cv.namedWindow(name, cv.WINDOW_AUTOSIZE)
        cv.imshow(name, np.hstack((self.imageColor, self.depthColormap)))
        keyCode = cv.waitKey(1)

        return None

    def end(self):
        self._pipeline.stop()
        print('[Info] - Realsense shuted down.')

        return None

if __name__ == '__main__':
    try:
        realCam = RealCam()
        while True:
            realCam.capture()
            realCam.show_video()
    except BaseException as err:
        print(err)
    finally:
        realCam.end()


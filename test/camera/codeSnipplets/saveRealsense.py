import pyrealsense2 as rs
import cv2 as cv
import numpy as np
from time import sleep

width = 1280 
height = 720
framerate = 30 

# initilize depth and color stream
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, framerate)
# config.enable_record_to_file('video1.bag')

# preparing video writer
out = cv.VideoWriter('videor.avi', cv.VideoWriter_fourcc(*'MJPG'),
        framerate-5, (width, height))

# start stream
pipeline.start(config)

try:
    while True:

        frames = pipeline.wait_for_frames()
        frameRGB = frames.get_color_frame()

        if not frameRGB:
            continue
        # conversion to numpy arrays
        imageRGB = np.asarray(frameRGB.get_data())
        
        # save to file
        out.write(imageRGB)
        # apply color map to depth image
        # cv.namedWindow('Realsense', cv.WINDOW_AUTOSIZE)
        # cv.imshow('Realssense', imageRGB)
        # cv.waitKey(1)
except Exception as e:
    print(str(e))
finally:
    pipeline.stop()
    out.release()

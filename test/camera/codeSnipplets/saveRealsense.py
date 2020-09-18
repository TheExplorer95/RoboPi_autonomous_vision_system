import pyrealsense2 as rs
import cv2 as cv
import numpy as np

width = 848 
height = 480
framerate = 30 

# initilize depth and color stream
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, framerate)
# config.enable_record_to_file('video1.bag')

# preparing video writer
out = cv.VideoWriter('videor.avi', cv.VideoWriter_fourcc(*'MJPG'), 23, (width, height))

# start stream
pipeline.start(config)

try:
    while True:

        frames = pipeline.wait_for_frames()
        frameRGB = frames.get_color_frame()

        if not frameRGB:
            print('nope')
            continue
        # conversion to numpy arrays
        imageRGB = np.asarray(frameRGB.get_data())
        
        # save to file
        out.write(imageRGB)
        
        # apply color map to depth image
        # cv.namedWindow('Realsense', cv.WINDOW_AUTOSIZE)
        # cv.imshow('Realssense', imageRGB)
        # cv.waitKey(1)

finally:
    pipeline.stop()
    cv.destroyAllWindows()
    out.release()

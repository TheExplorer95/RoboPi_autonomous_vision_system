import pyrealsense2 as rs
import cv2 as cv
import numpy as np

# initilize depth and color stream
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.yuyv, 30)

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

        # apply color map to depth image

        cv.namedWindow('Realsense', cv.WINDOW_AUTOSIZE)
        cv.imshow('Realssense', imageRGB)
        cv.waitKey(1)

except KeyboardInterrupt:
    print('[INFO] Shutting down camera')

finally:
    pipeline.stop()
    cv.destroyAllWindows()

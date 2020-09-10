import pyrealsense2 as rs
import cv2 as cv
import numpy as np

# initilize depth and color stream
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# start stream
pipeline.start(config)

try:
    while True:

        frames = pipeline.wait_for_frames()
        frameDepth = frames.get_depth_frame()
        frameRGB = frames.get_color_frame()

        if not frameDepth or not frameRGB:
            continue

        # conversion to numpy arrays
        imageDepth = np.asarray(frameDepth.get_data())
        imageRGB = np.asarray(frameRGB.get_data())

        # apply color map to depth image
        depthColormap = cv.applyColorMap(cv.convertScaleAbs(imageDepth, alpha=0.03), cv.COLORMAP_JET)

        cv.namedWindow('Realsense', cv.WINDOW_AUTOSIZE)
        cv.imshow('Realssense', np.hstack((imageRGB, depthColormap)))
        cv.waitKey(1)

except KeyboardInterrupt:
    print('[INFO] Shutting down camera')

finally:
    pipeline.stop()
    cv.destroyAllWindows()

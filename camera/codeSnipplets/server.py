import imagezmq
import cv2 as cv

imageHub = imagezmq.ImageHub()
cv.namedWindow('RPI stream', cv.WINDOW_NORMAL)
cv.resizeWindow('RPI stream', 800, 600)

while True:
    rpiName, frame = imageHub.recv_image()
    imageHub.send_reply(b'OK')

    cv.imshow('RPI stream', frame)
    cv.waitKey(1)

cv.destroyAllWindows()

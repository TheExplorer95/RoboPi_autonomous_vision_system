import cv2 as cv
import acapture as camera
import numpy as np

cap0 = camera.open(0)
cap1 = camera.open(1)

while True:
    check0, frame0 = cap0.read()
    check1, frame1 = cap1.read()
    if check0 and check1:
        frame0 = cv.cvtColor(frame0, cv2.COLOR_BGR2RGB)
        frame1 = cv.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        
        concat = np.hstack((frame0, frame1))

        cv.imshow('test', concat)
        cv.waitKey(1)

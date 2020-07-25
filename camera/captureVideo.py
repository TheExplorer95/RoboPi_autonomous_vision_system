import numpy as np
import cv2 as cv

cap0 = cv.VideoCapture(0)
#cap1 = cv.VideoCapture(1)

if not cap0.isOpened():
    print('[ERROR] Cannot open camera stream.')
    quit()

try:
    while True:
        ret0, frame0 = cap0.read()
        #ret1, frame1 = cap1.read()

        if not ret0:
            raise ValueError

        # show one camera
        cv.imshow('frame', frame0)

except KeyboardInterrupt:
    print('[INFO] Programm is shutting down')
except ValueError:
    print("[ERROR] Can't receive frame. Exiting...")
finally:
    cap0.release()
    #cap1.release()
    cv.destroyAllWindows()
    quit()


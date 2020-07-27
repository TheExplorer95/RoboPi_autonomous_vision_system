import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

cap = cv.VideoCapture('/dev/video2')
#cap1 = cv.VideoCapture(1)

if not cap.isOpened():
    print('[ERROR] Cannot open camera stream.')
    quit()

first = True

try:
    while True:
        ret, frame = cap.read()
        if first:
            print(type(frame))
            print(frame)
            print(frame.shape)
            first = False
            imgplot = plt.imshow(frame)
            plt.show()
        #ret1, frame1 = cap1.read()

        if not ret:
            raise ValueError

        # show one camera
        cv.imshow('Webcam Life2Coding', frame)
        cv.waitKey(1)
except KeyboardInterrupt:
    print('[INFO] Programm is shutting down')
except ValueError:
    print("[ERROR] Can't receive frame. Exiting...")
finally:
    cap.release()
    #cap1.release()
    cv.destroyAllWindows()
    quit()


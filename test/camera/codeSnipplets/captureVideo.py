import numpy as np
import cv2 as cv

try:
    # lock devices
    cap0 = cv.VideoCapture('/dev/video6')
    #cap1 = cv.VideoCapture('/dev/video7')
    
    # detect if connection was establish sucessfully
    if not cap0.isOpened(): #or not cap1.isOpened():
        print('[ERROR] Cannot open camera stream.')
        raise Exception
    
    # capture frames and show them
    while True:
        ret0, frame0 = cap0.read()
        #ret1, frame1 = cap1.read()
        
        # detect if stream is broken
        if not ret0: #or not ret1:
            raise ValueError

        cv.imshow('concat', frame0)
        cv.waitKey(1)
#        cv.imshow('first cam', frame0)
#        cv.waitKey(1)
#        cv.imshow('second cam', frame1)
#        cv.waitKey(1)

except KeyboardInterrupt:
    print('[INFO] Programm is shutting down')
except ValueError:
    print("[ERROR] Can't receive frame. Exiting...")
except Exception as e:
    print('Nope not working', e)
finally:
    cap0.release()
    #cap1.release()
    cv.destroyAllWindows()
    quit()


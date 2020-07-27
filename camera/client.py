from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

# setup argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-S', '--server-ip', required=True, help='ip adress of the server to which the client will connect')
args = vars(ap.parse_args())

# initialization of sender object
sender = imagezmq.ImageSender(connect_to='tcp://{}:5555'.format(args['server_ip']))

# initialize video capture objects
rpiName = socket.gethostname()
vs0 = VideoStream(src='/dev/video0').start()
vs1 = VideoStream(src='/dev/video1').start()

time.sleep(2.0)

try:
    while True:
        frame0 = vs0.read()
        frame1 = vs1.read()
        sender.send_image(rpiName, np.vstack((frame0, frame1)))
except KeyboardInterrupt:
    quit()

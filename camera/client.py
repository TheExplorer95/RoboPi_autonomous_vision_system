from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

ap = argparse.ArgumentParser()
ap.add_argument('-S', '--server-ip', required=True, help='ip adress of the server to which the client will connect')
args = vars(ap.parse_args())

sender = imagezmq.ImageSender(connect_to='tcp://{}:5555'.format(args['server_ip']))

rpiName = socket.gethostname()
vs0 = VideoStream(src=0).start()
vs1 = VideoStream(src=1).start()

time.sleep(2.0)

while True:
    frame0 = vs0.read()
    #frame1 = vs1.read()
    sender.send_image(rpiName, frame0)
    #sender.send_image(rpiName, frame1)



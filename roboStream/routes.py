from flask import Response, Flask, render_template
import pyrealsense2 as rs
import threading
import datetime
import imutils
import time
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

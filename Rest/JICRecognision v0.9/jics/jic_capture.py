# File: jic_capture.py

# Public libraries
import cv2 as cv
import pyrealsense2 as rs

# JIC libraries
from jic_settings import use_real_sense

# Define realsense variables
pipe = rs.pipeline()
cfg = rs.config()

# Define default variabes
video_id = 0
stream = cv.VideoCapture(video_id, cv.CAP_DSHOW)

width = 0
height = 0
fps = 0

# Initialize
def initialize():
    log("Initializing...")
    if(not use_real_sense):
        log("Using Default Camera")
        try:
            global stream, video_id
            if not is_ready() or (stream == None) or video_id < 0:
                log("Failed")
                return
            
            global width, height, fps
            stream.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
            stream.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

            width = int(stream.get(cv.CAP_PROP_FRAME_WIDTH))
            height = int(stream.get(cv.CAP_PROP_FRAME_HEIGHT))
            fps = int(stream.get(cv.CAP_PROP_FPS))
            log("Ready")
            return
        except:
            pass
        log("Failed")
    else:
        log("Using RealSense")
        try:
            cfg.enable_stream(rs.stream_color, 640, 480, rs.format.bgr8, 30)

            width = 640
            height = 480
            fps = 0

            pipe.start(cfg)

            log("Ready")
            return
        except:
            pass
        log("Failed")

# Check if stream is ready
def is_ready():
    global stream

    if(use_real_sense):
        return True
    
    # Check if stream is openend
    if not (stream.isOpened()):
        return False
    
    # Reading random frame (and data)
    read, frame = stream.read()
    if not read:
        return False
    return True

# Read stream
def read():
    if(use_real_sense):
        pipe.start(cfg)
        return True, pipe.wait_for_frames()
    else:
        return stream.read()


# Flush/Release the stream
def flush():
    if(use_real_sense):
        pipe.stop()
    else:
        stream.release()

# Log messages in console
def log(message):
    print(f"JIC_Capture: {message}")
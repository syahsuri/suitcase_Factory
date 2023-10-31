# File: jic_windows.py
import tkinter as tk

# Public libraries
import cv2 as cv
import numpy as np
import time

# JIC libraries
import jic_image
from jic_settings import read_cursor
from jic_capture import read

# Define variables
lower_rgb = np.array([0, 0, 0])
upper_rgb = np.array([255, 255, 255])
origin = (522, 140)
angle_x = 15 # Was 9
angle_y = 887

# Default values RGB
red = [0, 142]
green = [73, 255]
blue = [0, 255]

# Maximal windows size
max_size = [800, 800]

modifier_window = "JIC Modifier"
frame_viewer_window = "JIC Frame Viewer"

# Initialize
def initialize():
    log("Initializing...")

    convert_colors()

    cv.namedWindow(modifier_window)
    cv.resizeWindow(modifier_window, 400, 350)

    cv.namedWindow(frame_viewer_window, cv.WINDOW_NORMAL)
    cv.resizeWindow(frame_viewer_window, max_size[0], max_size[1])

    log("Ready")

# Perform on slider change
def on_slider_change(value, color_channel, range):
    global lower_rgb, upper_rgb
    changed = False
    if(range == 1):
        if not (upper_rgb[color_channel] == value):
            changed = True
        upper_rgb[color_channel] = value
    elif (range == 0):
        if not (upper_rgb[color_channel] == value):
            changed = True
        lower_rgb[color_channel] = value
    if (changed):
        log(f"Upper RGB: {upper_rgb} | Lower RGB: {lower_rgb}")

# Perform on slider change thresh
def on_angle_change(value, angle):
    global angle_x, angle_y
    if(angle == "x"):
        angle_x = value
    elif(angle == "y"):
        angle_y = value

# Return the RGB range values
def get_color_range():
    global upper_rgb, lower_rgb
    return [upper_rgb, lower_rgb]

# Return origin value
def get_origin_point():
    global origin
    return origin

# Return origin point
def get_origin():
    return origin

# Return angle values
def get_angles():
    global angle_x, angle_y
    return angle_x, angle_y

# Convert colors
def convert_colors():
    global red, green, blue, upper_rgb, lower_rgb
    lower_rgb = np.array([red[0], green[0], blue[0]])
    upper_rgb = np.array([red[1], green[1], blue[1]])

# Open settings modifier
def open_modifier():
    cv.createTrackbar("Max Red", modifier_window, red[1], 255, lambda x: on_slider_change(x, 0, 1))
    cv.createTrackbar("Min Red", modifier_window, red[0], 255, lambda x: on_slider_change(x, 0, 0))
    cv.createTrackbar("Max Green", modifier_window, green[1], 255, lambda x: on_slider_change(x, 1, 1))
    cv.createTrackbar("Min Green", modifier_window, green[0], 255, lambda x: on_slider_change(x, 1, 0))
    cv.createTrackbar("Max Blue", modifier_window, blue[1], 255, lambda x: on_slider_change(x, 2, 1))
    cv.createTrackbar("Min Blue", modifier_window, blue[0], 255, lambda x: on_slider_change(x, 2, 0))
    cv.createTrackbar("Angle X", modifier_window, angle_x, 3600, lambda x: on_angle_change(x, "x"))
    cv.createTrackbar("Angle Y", modifier_window, angle_y, 3600, lambda x: on_angle_change(x, "y"))

# Open frame viewer
def open_frame_viewer(frame, name=frame_viewer_window):
    # Resize frame to fit window
    frame = jic_image.resize(frame, max_size[0], max_size[1])

    # Resize to fit image
    if check_window(name):
        cv.resizeWindow(name, frame.shape[1], frame.shape[0])
    else:
        cv.namedWindow(name, cv.WINDOW_NORMAL)

    # Show the current frame with text
    if check_window(name):
        cv.imshow(name, frame)
    
    if read_cursor:
        cv.setMouseCallback(frame_viewer_window, get_mouse_data)

# Check if window exists
def check_window(window):
    try:
        rect = cv.getWindowImageRect(window)
        if rect[0] == -1:
            return False
        return True
    except:
        return False

# Destroy all windows
def close_windows():
    cv.destroyAllWindows()

# Destroy window
def close_window(window):
    cv.destroyWindow(window)

# Check if stream is ready
def is_ready():
    return True

# Log messages in console
def log(message):
    print(f"JIC_Windows: {message}")

# Mouse callback function get the position
def get_mouse_data(event, x, y, flags, param):
    #if event == cv.EVENT_LBUTTONDBLCLK:
        #print(f"Position at (x={x}, y={y})")
    if event == cv.EVENT_LBUTTONDOWN:
        global origin
        origin = (x, y)
        print(f"Adjusting origin to (x={x}, y={y})")
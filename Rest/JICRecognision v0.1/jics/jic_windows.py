# File: jic_windows.py

# Public libraries
import cv2 as cv
import numpy as np

# JIC libraries
import jic_image

# Define variables
lower_rgb = np.array([0, 0, 0])
upper_rgb = np.array([255, 255, 255])

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
    cv.resizeWindow(modifier_window, 400, 250)

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

# Return the RGB range values
def color_range():
    global upper_rgb, lower_rgb
    return [upper_rgb, lower_rgb]

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

# Open frame viewer
def open_frame_viewer(frame):
    # Resize frame to fit window
    frame = jic_image.resize(frame, max_size[0], max_size[1])

    # Display frame name
    #frame_name = "Default Value" #video.frame_names[video.current_frame_index]
    #cv.putText(frame, frame_name, (10, 30), cv.FONT_HERSHEY_COMPLEX , 0.8, (0, 0, 0), 4, cv.LINE_AA)
    #cv.putText(frame, frame_name, (10, 30), cv.FONT_HERSHEY_COMPLEX , 0.8, (255, 255, 255), 2, cv.LINE_AA)

    # Resize to fit image
    if check_window(frame_viewer_window):
        cv.resizeWindow(frame_viewer_window, frame.shape[1], frame.shape[0])

    # Show the current frame with text
    if check_window(frame_viewer_window):
        cv.imshow(frame_viewer_window, frame)

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
# File: main.py

# Public libraries
import sys
import os
import cv2 as cv
import time

# Import JIC libraries
sys.path.append(os.getcwd() + "\\OpenCV\\JICRecognision\\jics")

# JIC libraries
import jic_windows
import jic_capture
import jic_image
import jic_preproces
import jic_postproces
import jic_algorhythms
import jic_calibrate
import jic_socket
from jic_settings import read_cursor, display_modifier

# Initialize
def initialize():
    os.system('cls')
    print("Initializing...")

    # Initializing calibrate
    jic_calibrate.initialize()
    if not jic_calibrate.is_ready():
        disable()
        return
    
    # Initializing capture stream
    jic_capture.initialize()
    if not jic_capture.is_ready():
        disable()
        return

    # Initializing image
    jic_image.initialize()
    if not jic_image.is_ready():
        disable()
        return
    
    # Initializing preproces
    jic_preproces.initialize()
    if not jic_preproces.is_ready():
        disable()
        return

    # Initializing postproces
    jic_postproces.initialize()
    if not jic_postproces.is_ready():
        disable()
        return
    
    # Initializing algorhythms
    jic_algorhythms.initialize()
    if not jic_algorhythms.is_ready():
        disable()
        return

    # Initializing windows
    jic_windows.initialize()
    if not jic_windows.is_ready():
        disable()
        return

    # Initializing socket
    jic_socket.initialize()
    if not jic_socket.is_ready():
        disable()
        return
    
    if read_cursor:
        log("Enabled cursor reading")
        cv.setMouseCallback(jic_windows.frame_viewer_window, get_mouse_coordinates)

    if display_modifier:
        log("Enabled modifier")
        jic_windows.open_modifier()
    else:
        pass
        jic_windows.close_window(jic_windows.modifier_window)

    log("Ready")
    main()


def main():

    # Send/Receive test message
    jic_socket.send_message("hello there!")
    jic_socket.receive_message()

    while(True):
        # Reading latest frame (and data)
        read, frame = jic_capture.read()
        if not read:
            break

        # Set canvas
        image = frame

        # Apply preproces
        image, frame = jic_preproces.proces(image, frame)

        # Apply postproces
        image, frame = jic_postproces.proces(image, frame)

        # Apply algorhythms
        image, frame = jic_algorhythms.proces(image, frame)

        # View frame
        jic_windows.open_frame_viewer(image.copy())

        # Key down detection
        key = cv.waitKey(1)
        if key == 27: # esc
            break

        # Wait a second
        time.sleep(0.1)
    
    disable()

# Get mouse coordinates
def get_mouse_coordinates(event, x, y, flags, param):
    if event == cv.EVENT_MOUSEMOVE:
        print(f"Mouse Coordinates: (x={x}, y={y})")

# Disable program
def disable():
    log("Disabling...")
    # Flush stream
    jic_capture.flush()

    # Close all windows
    jic_windows.close_windows()
    log("Disabled")
    exit()

# Log messages in console
def log(message):
    print(f"{message}")

initialize()
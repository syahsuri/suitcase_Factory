# File: jic_preproces.py

# Import libraries
from jic_settings import original_view

# Define global variables
crops = [0, 0, 0, 0]

# Initialize
def initialize():
    log("Initializing...")
    
    log("Ready")

# Processes all pre processes
def proces(image, canvas):
    # Undistort image
    canvas = undistort(canvas)

    # Crop image to desired size and ratio
    canvas = crop(canvas, 110, 40, 640, 480)

    # Return result
    return image, canvas

# Undistort image
def undistort(image):
    return image

# Crop image
def crop(image, x, y, w, h):
    global crops
    crops = [x, y, w, h]
    region_of_interest = image[y:y+h, x:x+w]
    return region_of_interest

def get_crop_point():
    return crops[0], crops[1]

def get_crop_points():
    return crops

# Check if stream is ready
def is_ready():
    return True

# Log messages in console
def log(message):
    print(f"JIC_Preproces: {message}")
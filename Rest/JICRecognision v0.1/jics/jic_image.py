# File: jic_image.py

# Public libraries
import cv2 as cv

# Initialize
def initialize():
    log("Initializing...")
    
    log("Ready")

# Resize display window
def resize(image, width, height):
    aspect_ratio = image.shape[1] / image.shape[0]
    target_aspect_ratio = width / height

    if aspect_ratio > target_aspect_ratio:
        new_width = width
        new_height = int(width / aspect_ratio)
    else:
        new_width = int(height * aspect_ratio)
        new_height = height

    resized_image = cv.resize(image, (new_width, new_height))
    return resized_image

# Check if stream is ready
def is_ready():
    return True

# Log messages in console
def log(message):
    print(f"JIC_Image: {message}")
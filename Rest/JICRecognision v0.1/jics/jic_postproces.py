# File: jic_postproces.py

# Public libraries
import cv2 as cv

# Import libraries
from jic_settings import original_view, draw_crop
from jic_preproces import get_crop_points
from jic_windows import color_range

# Initialize
def initialize():
    log("Initializing...")
    
    log("Ready")

# Processes all post processes
def proces(image, frame):
    # Remove greenscreen
    frame = chroma_key(frame)

    # Draw crop outline
    if original_view:
        if (draw_crop):
            frame = draw_crop(frame)

    # Return result
    if not original_view:
        image = frame
    return image, frame

# Chroma key image
def chroma_key(image):
    upper = color_range()[0]
    lower = color_range()[1]

    mask = cv.inRange(image, lower, upper)
    output_image = cv.cvtColor(image, cv.COLOR_RGB2BGRA)
    output_image[mask > 0] = [0, 0, 0, 0] # 0, 0, 255, 0 for Red
    return output_image

def draw_crop(image):
    crops = get_crop_points()
    if len(crops) != 4:
        raise ValueError("The 'crops' list must contain 4 coordinates (x1, y1, x2, y2)")
    x1, y1, x2, y2 = crops
    image = cv.rectangle(image, (0, 0), (x2, y2), (0, 0, 255), 5)
    return image

# Check if stream is ready
def is_ready():
    return True

# Log messages in console
def log(message):
    print(f"JIC_Postproces: {message}")
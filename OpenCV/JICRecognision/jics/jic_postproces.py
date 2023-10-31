# File: jic_postproces.py

# Public libraries
import cv2 as cv
import numpy as np
import math

# Import libraries
from jic_socket import send_command
from jic_settings import original_view, draw_crop, display_los
from jic_preproces import get_crop_points
from jic_windows import get_color_range, get_angles, get_origin
from jic_calibrate import convert_to_world
import jic_socket

# Define default variables
min_pixel_count = 200
max_pixel_count = 700

# Initialize
def initialize():
    log("Initializing...")
    
    log("Ready")

# Processes all post processes
def proces(image, canvas):
    # Remove greenscreen
    #canvas = chroma_key(canvas)

    # Draw crop outline
    #if original_view:
        #if (draw_crop):
            #canvas = draw_crop(canvas)

    original_canvas = canvas.copy()
    canvas, point = draw_point(canvas, get_origin())
    canvas, line_points_x = draw_line(canvas, point, (get_angles()[0]/10), 900, color=(255, 0, 0))
    canvas, line_points_y = draw_line(canvas, point, (get_angles()[1]/10), 800, color=(0, 255, 0))
    proces_data(original_canvas, line_points_x, line_points_y)

    # Return result
    return image, canvas

# Draw point
def draw_point(image, point):
    image = cv.circle(image, point, 3, (0, 0, 255), 2)
    return image, point

# Draw line
def draw_line(image, fixed_point, angle, length, color=(0, 0, 255)):
    angle_rad = angle * math.pi / 180.0
    x2 = int(round(fixed_point[0] + length * math.cos(angle_rad)))
    y2 = int(round(fixed_point[1] + length * math.sin(angle_rad)))

    image = cv.line(image, fixed_point, (x2, y2), color, 3)
    line_points = (fixed_point, (x2, y2))
    return image, line_points

retry = False
# Proces and send data
def proces_data(image, line_points_x, line_points_y):
    global retry
    
    log("Scanning for frames...")
    width = get_frame_length(image, line_points_x, "x") #pi
    height = get_frame_length(image, line_points_y, "y") #pi

    # Send/Receive test message
    command = jic_socket.wait_for_command()
    if((command == "start" and jic_socket.online_mode) or retry):
    
        if not (is_valid(width, height)):
            retry = True
            return
        size = width, height
        log(f"Size (wxh): {size}pi")
        width, height = convert_to_world(width, height) #m
        size = width/100, height/100
        log(f"Size (wxh): {size}m")
        sizes = str(size)

        send_command(sizes)
        retry = False

# Get frame length
def get_frame_length(image, line_points, direction = "x"):
    # Create a mask with a single channel for alpha
    mask = np.zeros((*image.shape[:2], 1), dtype=np.uint8)
    cv.line(mask, line_points[0], line_points[1], 255, 1)

    # Apply the mask to the masked_image
    result = cv.bitwise_and(image, image, mask=mask)

    pixels = get_line_of_sight(result)
    length = get_last_pixel(pixels, direction)

    if display_los:
        modified_pixels = get_color_strip(pixels, direction)
        display_line_of_sight(modified_pixels, direction)
    return length

# Transform line of sight to list
def get_line_of_sight(image):
    non_transparent_pixels = image[~np.all(image == [0, 0, 0], axis=-1), :3]
    return non_transparent_pixels.tolist()

# Detect if pixel is part of frame
def is_frame(pixel, direction):
    blackish_threshold = 70
    is_blackish = all(channel <= blackish_threshold for channel in pixel)
    return is_blackish or (is_silverish(pixel) and direction == "x")

# Detect if pixel is silverish and not table color
def is_silverish(pixel):
    tolerance = 22 # was 23
    silver_color = [163, 146, 120]
    #silver_color = [189, 170, 137] OLD BUT WORKING
    max_diff = tolerance
    is_silver = all(abs(pixel[i] - silver_color[i]) <= max_diff for i in range(3))
    return is_silver

# Get last frame pixel
def get_last_pixel(pixels, direction):
    global min_pixel_count
    i = 0
    last_pixel = 0
    for pixel in pixels:
        if(i > min_pixel_count):
            if is_frame(pixel, direction):
                last_pixel = i
        i = i + 1
    return last_pixel

# Get color strip of line of sight
def get_color_strip(pixels, direction):
    global min_pixel_count
    red_color = [0, 0, 255]
    modified_pixels = []
    i = 0
    last_pixel = 0
    for pixel in pixels:
        modified_pixels.append(pixel)
        if(i > min_pixel_count):
            if is_frame(pixel, direction):
                last_pixel = i
        i = i + 1
    modified_pixels[last_pixel] = red_color
    return modified_pixels

# Display line of sight in window
def display_line_of_sight(pixels, direction):
    line_width = len(pixels)
    image = np.zeros((7, line_width, 3), dtype=np.uint8)
    for x in range(line_width):
        pixel = pixels[x]
        image[1:7, x] = pixel
    cv.imshow(f"Line of Sight {direction}", image)

# Chroma key image
def chroma_key(image):
    upper = get_color_range()[0]
    lower = get_color_range()[1]

    mask = cv.inRange(image, lower, upper)
    output_image = cv.cvtColor(image, cv.COLOR_RGB2BGRA)
    output_image[mask > 0] = [0, 0, 0, 0] # 0, 0, 255, 0 for Red
    return output_image

# Draw crop
def draw_crop(image):
    crops = get_crop_points()
    if len(crops) != 4:
        raise ValueError("The 'crops' list must contain 4 coordinates (x1, y1, x2, y2)")
    x1, y1, x2, y2 = crops
    image = cv.rectangle(image, (0, 0), (x2, y2), (0, 255, 0), 5)
    return image

# Check if size is valid
def is_valid(width, height):
    global min_pixel_count, max_pixel_count
    if(width <= min_pixel_count or height <= min_pixel_count):
        log("Invalid size (too small), retrying...")
        return False
    if(width > max_pixel_count or height > max_pixel_count):
        log("Invalid size (too big), retrying...")
        return False
    return True

# Check if stream is ready
def is_ready():
    return True

# Log messages in console
def log(message):
    print(f"JIC_Postproces: {message}")
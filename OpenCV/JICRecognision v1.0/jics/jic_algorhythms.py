# File: jic_algorhythms.py 

# Public libraries
import cv2 as cv
import numpy as np

# JIC libraries
import jic_calibrate
from jic_preproces import get_crop_point

# Initialize
def initialize():
    log("Initializing...")

    log("Ready")

# Processes all algorhythms processes
def proces(image, canvas):
    # Frame Detect
    canvas, points = frame_detect(canvas)
    if not isinstance(points, np.ndarray):
        return image, canvas
    
    # Read canvas size
    width, height = calculate_rectangle_sizes(points)

    # Calibrate size
    width, height = jic_calibrate.convert_to_world(width, height)

    # Correct size
    width = jic_calibrate.correct(width)
    height = jic_calibrate.correct(height)
    inner_points = jic_calibrate.shrink(points)

    # Draw
    canvas = draw_frame(canvas, points)
    canvas = draw_frame(canvas, inner_points)
    canvas = draw_size(canvas, width, height)

    # Return result
    return image, canvas

# Detect frame
def frame_detect(image):
    mask = image[:, :, 3] # Normally 2 must be 3
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        return image, None

    largest_contour = max(contours, key=cv.contourArea)
    min_rect = cv.minAreaRect(largest_contour)

    result_image = image.copy()
    points = cv.boxPoints(min_rect).astype(np.int32)
    return result_image, points

# Calculate rectangle size
def calculate_rectangle_sizes(points):
    points = np.array(points)
    center = np.mean(points, axis=0)
    angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])

    top_left_index = np.argmin(angles)

    width = np.linalg.norm(points[top_left_index] - points[(top_left_index + 1) % 4])
    height = np.linalg.norm(points[top_left_index] - points[(top_left_index + 3) % 4])

    return width, height

# Draw frame contour
def draw_frame(image, points):
    crop = get_crop_point()
    points = move_points(points, crop[0], crop[1])
    image = cv.drawContours(image, [points], 0, (0, 0, 255), 1)
    return image

# Draw frame size
def draw_size(image, width, height):
    text = f"Width: {round(width, 2)}{jic_calibrate.unit}, Height: {round(height, 2)}{jic_calibrate.unit}"
    image = cv.putText(image, text, (10, image.shape[0] - 15), cv.FONT_HERSHEY_COMPLEX , 0.4, (0, 0, 0), 2, cv.LINE_AA)
    image = cv.putText(image, text, (10, image.shape[0] - 15), cv.FONT_HERSHEY_COMPLEX , 0.4, (255, 255, 255), 1, cv.LINE_AA)
    return image

# Move points after preproces
def move_points(points, x, y):
    if len(points) != 4:
        raise ValueError("Input must be a list of 4 corner points")

    for i in range(len(points)):
        xx, yy = points[i]
        moved_point = [xx + x, yy + y]
        points[i] = moved_point
    
    return points

# Check if stream is ready
def is_ready():
    return True

# Log messages in console
def log(message):
    print(f"JIC_Algorhythms: {message}")
# File: jic_calibrate.py 

# Import libraries
import math
import numpy as np

# Define global correction value
correction = 1.573 #GREENSCREEN

# Define global scaling factors
unit = "cm"
enable_size_1 = True
camera_size_1 = [575, 442]
world_size_1 = [47.8, 37.05] # Default L shape
enable_size_2 = True
camera_size_2 = [544, 346]
world_size_2 = [44.8, 28.6] # Medium square shape
enable_size_3 = True
camera_size_3 = [601, 441]
world_size_3 = [49.8, 36.35] # Black default square shape

# Define global variables
width_scaling_factor = 0
height_scaling_factor = 0

calibrate_error = False

# Initialize
def initialize():
    log("Initializing...")
    
    if not (calibrate()):
        log("Failed")
        return 
    log("Ready")

# Calibrate
def calibrate():
    global calibrate_error, width_scaling_factor, height_scaling_factor
    global camera_size_1, camera_size_2, camera_size_3
    global world_size_1, world_size_2, world_size_3
    
    try:
        div = 0
        width_scale_1 = world_size_1[0] / camera_size_1[0]
        height_scale_1 = world_size_1[1] / camera_size_1[1]
        if not (enable_size_1):
            width_scale_1 = 0
            height_scale_1 = 0
        else:
            div = div + 1
        width_scale_2 = world_size_2[0] / camera_size_2[0]
        height_scale_2 = world_size_2[1] / camera_size_2[1]
        if not (enable_size_2):
            width_scale_2 = 0
            height_scale_2 = 0
        else:
            div = div + 1
        width_scale_3 = world_size_3[0] / camera_size_3[0]
        height_scale_3 = world_size_3[1] / camera_size_3[1]
        if not (enable_size_3):
            width_scale_3 = 0
            height_scale_3 = 0
        else:
            div = div + 1

        if(div < 1):
            return False
        
        width_scaling_factor = (width_scale_1 + width_scale_2 + width_scale_3)/div
        height_scaling_factor = (height_scale_1 + height_scale_2 + height_scale_3)/div

        calibrate_error = False
        return True
    except:
        calibrate_error = True
        return False

# Convert from camera size to world size
def convert_to_world(camera_width, camera_height):
    global width_scaling_factor, height_scaling_factor
    world_width = camera_width * width_scaling_factor
    world_height = camera_height * height_scaling_factor
    return world_width, world_height

# Convert from camera size to world size
def convert_to_camera(world_width, world_height):
    global width_scaling_factor, height_scaling_factor
    camera_width = world_width / width_scaling_factor
    camera_height = world_height / height_scaling_factor
    return camera_width, camera_height

# Correct values (Apply value decreasements)
def correct(value):
    return (value - 2*correction)

# Shrink detection frame
def shrink(points):
    if len(points) != 4:
        raise ValueError("Input must be a list of 4 corner points")
    val = convert_to_camera(correction, correction)[0]
    amount = math.sqrt(val ** 2 + val ** 2)
    points = np.array(points, dtype=float)
    center = np.mean(points, axis=0)
    
    for i in range(len(points)):
        direction = center - points[i]
        direction /= np.linalg.norm(direction)
        points[i] += direction * amount
    points = np.round(points).astype(int)
    
    return points

# Check if stream is ready
def is_ready():
    global calibrate_error
    check_1 = check_negative_or_zero(camera_size_1)
    check_2 = check_negative_or_zero(world_size_1)
    check_3 = check_negative_or_zero(camera_size_2)
    check_4 = check_negative_or_zero(world_size_2)
    check_5 = check_negative_or_zero(camera_size_3)
    check_6 = check_negative_or_zero(world_size_3)
    
    if(calibrate_error):
        return False
    if check_1 or check_2 or check_3 or check_4 or check_5 or check_6:
        return False
    if(width_scaling_factor == 0 or height_scaling_factor == 0):
        return False
    return True

# Check if negative or zero
def check_negative_or_zero(values):
    for value in values:
        if value <= 0:
            return True
    return False

# Log messages in console
def log(message):
    print(f"JIC_Calibrate: {message}")
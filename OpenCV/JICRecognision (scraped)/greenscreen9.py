#Fix distortion
#minAreaRect

# Imported libraries
import cv2 as cv
import numpy as np
import time

# Declaration of variables
hough_threshold = 150

lower_green = np.array([30, 30, 0])
upper_green = np.array([104, 255, 104])

# Declare and import video/image material
vid = cv.VideoCapture(1)
frame = None
#frame = cv.imread("OpenCV\greenscreen_grey.jpg")

# Frame process display
frames = []
frame_names = []
current_frame_index = 0

# Display window size
window_width = 800
window_height = 600

# Main code
def main():
    # Define global variables
    global frame, current_frame_index

    # Open a window for the adjustable trackbar
    open_modifier()

    # Capture the video frame by frame
    retTest, frameTest = vid.read()

    # Check if a frame was successfully captured
    if not retTest:
        return
    
    first_frame = frameTest

    #Add first frame
    imadd("Original #0", first_frame)
    
    while True:
        # Capture the video frame by frame
        ret, frame = vid.read()

        # Check if a frame was successfully captured
        if not ret:
            break
    
        original_frame = frame
        modified_frame = frame

        # Apply post processing
        #modified_frame = apply_post_processing(original_frame)

        # Apply OpenCV algorhythms
        #modified_frame = apply_opencv_algorithms(modified_frame)

        # Open/Update frame viewer for live footage of the process steps
        print("Update frame")
        update_frame_viewer()
        open_frame_viewer()

        # Detect keys
        key = cv.waitKey(1)
        #if key == -1:
        #    print("Closing down")
        #    break
        # '>' key
        if key == 46:
            current_frame_index = (current_frame_index + 1) % len(frames)
        # '<' key
        elif key == 44:
            current_frame_index = (current_frame_index - 1) % len(frames)

        # Wait a second
        time.sleep(0.1)

    # Release video
    vid.release()

    # Close all windows
    cv.destroyAllWindows()

# Functions

# Apply Post Processing
def apply_post_processing(image):
    # Define global variables
    global frames, current_frame_index
    global lower_green, upper_green

    # Create a mask for the background
    green_mask = cv.inRange(image, lower_green, upper_green)
    imadd("Green Mask #1", green_mask)

    # Create a mask for the object in front of the background
    object_mask = cv.inRange(image, np.array([0, 0, 0]), np.array([100, 100, 100]))
    imadd("Object Mask #2", object_mask)

    # Combine the green screen mask and the object mask
    mask = cv.bitwise_and(green_mask, cv.bitwise_not(object_mask))
    imadd("Mask #3", mask)

    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)

    # Dilate mask
    mask = cv.dilate(mask, kernel, iterations=1)
    imadd("Dilated Mask #4", mask)

    # Erode mask
    mask = cv.erode(mask, kernel, iterations=1)
    imadd("Eroded Mask #5", mask)

    # Combine mask with original image
    frame_mask = cv.bitwise_and(image, image, mask=mask)
    imadd("Mask #6", frame_mask)

    # Create a red replacement for the green pixels
    red_pixels = np.zeros_like(image)
    red_pixels[mask > 0] = [0, 0, 255]
    imadd("Cut Out Area #7", red_pixels)

    # Subtract the green-shaded pixels and add red pixels
    comb_frame = image - frame_mask + red_pixels
    imadd("Object On Cut Out #8", comb_frame)

    # Replace red pixels with alpha 255 pixels
    alpha_frame = alphanize(comb_frame)
    imadd("Alpha Post Result #9", alpha_frame)

    # Apply Gaussian blur
    gaussian_frame = cv.GaussianBlur(alpha_frame, (5, 5), 5)
    imadd("Gaussian Blur Result #10", gaussian_frame)

    output_frame = gaussian_frame
    return output_frame

# Apply OpenCV Algorythms
def apply_opencv_algorythms(image):
    # Define global variables
    global frames

    # Perform Canny edge detection
    canny_frame = canny_edge_detection(image)
    imadd("Canny Edge Result #11", canny_frame)

    # Perform Hough line detection
    hough_frame = hough_line_detection(canny_frame)
    imadd("Hough Line Result #12", hough_frame)

    output_image = hough_frame
    return output_image

# Upon changing the value of the lower green threshold
def on_lower_green(value):
    global lower_green
    lower_green[1] = value
    update_frame_viewer()

# Upon changing the value of the lower green threshold
def on_upper_green(value):
    global upper_green
    upper_green[1] = value
    update_frame_viewer()

# Callback function for the Hough threshold trackbar
def on_hough_threshold(value):
    global hough_threshold
    hough_threshold = value
    update_frame_viewer()

# Replace any pure red pixels with alpha 255 pixels
def alphanize(image):
    red_lower = np.array([0, 0, 200])
    red_upper = np.array([100, 100, 255])
    mask = cv.inRange(image, red_lower, red_upper)
    output_image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)
    output_image[mask > 0] = [0, 0, 0, 0]
    return output_image

# Canny edge algorhythm
def canny_edge_detection(image):
    # Apply Canny algorhythms
    output_image = cv.Canny(image, 50, 200, None, 3)
    return output_image

# Hough line algorhythm
def hough_line_detection(image):
    output_image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)

    lines = cv.HoughLines(image, 1, np.pi / 180, hough_threshold, None, 0, 0)

    if lines is not None:
        height, width = image.shape[:2]  # Get the image dimensions

        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho

            # Calculate the endpoints of the line extending across the image
            x1 = int(x0 + width * (-b))
            y1 = int(y0 + width * (a))
            x2 = int(x0 - width * (-b))
            y2 = int(y0 - width * (a))

            cv.line(output_image, (x1, y1), (x2, y2), (0, 0, 255), 1, cv.LINE_AA)

    return output_image

# Resize display window
def imresize(image):
    # Define global variables
    global window_width, window_height

    max_width = window_width
    max_height = window_height
    aspect_ratio = image.shape[1] / image.shape[0]

    if image.shape[0] > max_height:
        image = cv.resize(image, (int(max_height * aspect_ratio), max_height))
    if image.shape[1] > max_width:
        image = cv.resize(image, (max_width, int(max_width / aspect_ratio)))
    return image

# Add frames to list
def imadd(title, image):
    image = imresize(image)
    frames.append(image)
    frame_names.append(title)

# Update frame viewer
def update_frame_viewer():
    # Define global variables
    global frame, frames

    # Check to not delete null
    if not frames:
        return
    
    original_frame = frame
    modified_frame = frame

    # Clear current list
    frames.clear()
    frame_names.clear()

    # Add original frame
    imadd("Original #0", original_frame)

    # Apply post processing
    modified_frame = apply_post_processing(modified_frame)

    # Apply OpenCV algorhythms
    modified_frame = apply_opencv_algorythms(modified_frame)

    # Reopen frame viewer on same index
    #open_frame_viewer()

# Open frame viewer
def open_frame_viewer():
    # Define global variables
    global frames, frame_names, current_frame_index

    cv.namedWindow("Frame Viewer", cv.WINDOW_NORMAL)

    first_frame = frames[0].copy()
    frame_height, frame_width, _ = first_frame.shape
    cv.resizeWindow("Frame Viewer", frame_width, frame_height)
    
    #while True:
    current_frame = frames[current_frame_index].copy()

    # Display frame name
    frame_name = frame_names[current_frame_index]
    cv.putText(current_frame, frame_name, (10, 30), cv.FONT_HERSHEY_COMPLEX , 0.8, (0, 0, 0), 4, cv.LINE_AA)
    cv.putText(current_frame, frame_name, (10, 30), cv.FONT_HERSHEY_COMPLEX , 0.8, (255, 255, 255), 2, cv.LINE_AA)

    # Show the current frame with text
    cv.imshow("Frame Viewer", current_frame)

# Open settings modifier
def open_modifier():
    # Define global variables
    global lower_green, upper_green, hough_threshold

    # Name window
    cv.namedWindow("Modifier")
    cv.resizeWindow("Modifier", 400, 200)

    # Create trackbars with default values
    initial_lower_green_value = 60  # Adjust this value as needed
    initial_upper_green_value = 255  # Adjust this value as needed
    initial_hough_threshold = 150  # Default Hough threshold value

    cv.createTrackbar("Min. Green Value", "Modifier", initial_lower_green_value, 255, on_lower_green)
    cv.createTrackbar("Max. Green Value", "Modifier", initial_upper_green_value, 255, on_upper_green)
    cv.createTrackbar("Hough Threshold", "Modifier", initial_hough_threshold, 500, on_hough_threshold)

main()
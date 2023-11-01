import cv2
import numpy as np

l_green = np.array([30, 30, 0])
u_green = np.array([104, 255, 104])  # Expanded upper threshold values

def on_lower_green(value):
    global l_green
    l_green[1] = value
    update_image()

def on_upper_green(value):
    global u_green
    u_green[1] = value
    update_image()

# Create a named window for the trackbars
cv2.namedWindow("Adjust Green Threshold")

# Create trackbars for the lower and upper green values (0-255) with default values
initial_lower_green_value = 60  # Adjust this value as needed
initial_upper_green_value = 255  # Adjust this value as needed

cv2.createTrackbar("Lower Green Value", "Adjust Green Threshold", initial_lower_green_value, 255, on_lower_green)
cv2.createTrackbar("Upper Green Value", "Adjust Green Threshold", initial_upper_green_value, 255, on_upper_green)

# Read the image
frame = cv2.imread("OpenCV/greenscreen_grey.jpg")

# Calculate the maximum display size while maintaining the aspect ratio
max_width = 800
max_height = 600
aspect_ratio = frame.shape[1] / frame.shape[0]

if frame.shape[0] > max_height:
    frame = cv2.resize(frame, (int(max_height * aspect_ratio), max_height))
if frame.shape[1] > max_width:
    frame = cv2.resize(frame, (max_width, int(max_width / aspect_ratio)))

def update_image():
    global frame, u_green, l_green
    mask = cv2.inRange(frame, l_green, u_green)
    
    # Create a mask for the object in front of the green screen
    object_mask = cv2.inRange(frame, np.array([0, 0, 0]), np.array([100, 100, 100]))  # Adjust the threshold values for the object color
    
    # Combine the green screen mask and the object mask
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(object_mask))
    
    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)
    
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Create a red replacement for the green pixels
    red_pixels = np.zeros_like(frame)
    red_pixels[mask > 0] = [0, 0, 255]

    # Subtract the green-shaded pixels and add red pixels
    result_image = frame - res + red_pixels

    cv2.imshow("Masked Image", result_image)

# Initial update
update_image()

while True:
    key = cv2.waitKey(10)
    if key == 27:
        break

cv2.destroyAllWindows()


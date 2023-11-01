import cv2
import numpy as np

l_green = np.array([30, 30, 0])
u_green = np.array([104, 153, 70])
l_red = np.array([0, 0, 0])
u_red = np.array([255, 255, 255])
l_blue = np.array([0, 0, 0])
u_blue = np.array([255, 255, 255])

def on_lower_green(value):
    global l_green
    l_green[1] = value
    update_image()

def on_upper_green(value):
    global u_green
    u_green[1] = value
    update_image()

def on_lower_red(value):
    global l_red
    l_red[2] = value
    update_image()

def on_upper_red(value):
    global u_red
    u_red[2] = value
    update_image()

def on_lower_blue(value):
    global l_blue
    l_blue[0] = value
    update_image()

def on_upper_blue(value):
    global u_blue
    u_blue[0] = value
    update_image()

# Create a named window for the trackbars
cv2.namedWindow("Adjust Color Thresholds")

# Create trackbars for the green values
cv2.createTrackbar("Lower Green Value", "Adjust Color Thresholds", l_green[1], 255, on_lower_green)
cv2.createTrackbar("Upper Green Value", "Adjust Color Thresholds", u_green[1], 255, on_upper_green)

# Create trackbars for the red values
cv2.createTrackbar("Lower Red Value", "Adjust Color Thresholds", l_red[2], 255, on_lower_red)
cv2.createTrackbar("Upper Red Value", "Adjust Color Thresholds", u_red[2], 255, on_upper_red)

# Create trackbars for the blue values
cv2.createTrackbar("Lower Blue Value", "Adjust Color Thresholds", l_blue[0], 255, on_lower_blue)
cv2.createTrackbar("Upper Blue Value", "Adjust Color Thresholds", u_blue[0], 255, on_upper_blue)

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
    global frame, u_green, l_green, u_red, l_red, u_blue, l_blue
    mask_green = cv2.inRange(frame, l_green, u_green)
    mask_red = cv2.inRange(frame, l_red, u_red)
    mask_blue = cv2.inRange(frame, l_blue, u_blue)
    
    mask = mask_green | mask_red | mask_blue
    
    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)
    
    # Apply Gaussian blur
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Create replacement colors for the removed pixels
    replacement_color = np.zeros_like(frame)
    replacement_color[mask_green > 0] = [0, 0, 255]  # Red for green pixels
    replacement_color[mask_red > 0] = [0, 255, 0]  # Green for red pixels
    replacement_color[mask_blue > 0] = [255, 0, 0]  # Blue for blue pixels

    # Subtract the green, red, and blue-shaded pixels and add replacement colors
    result_image = frame - res + replacement_color

    cv2.imshow("Original Image", frame)
    cv2.imshow("Masked Image", result_image)

# Initial update
update_image()

while True:
    key = cv2.waitKey(10)
    if key == 27:
        break

cv2.destroyAllWindows()

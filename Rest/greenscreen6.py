import cv2
import numpy as np

def replace_red_with_transparency(input_image):
    # Define the red color range you want to replace
    red_lower = np.array([0, 0, 200])  # Replace pure red pixels
    red_upper = np.array([100, 100, 255])  # Adjust the upper range as needed

    # Create a mask to identify red pixels within the specified range
    mask = cv2.inRange(input_image, red_lower, red_upper)

    # Create a copy of the input image as an RGBA image with a fully transparent alpha channel
    output_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2BGRA)

    # Set the alpha channel to 0 for the identified red pixels
    output_image[mask > 0] = [0, 0, 0, 0]

    return output_image

l_green = np.array([30, 30, 0])
u_green = np.array([104, 255, 104])  # Expanded upper threshold values
hough_threshold = 150  # Default Hough threshold value

def on_lower_green(value):
    global l_green
    l_green[1] = value
    update_image()

def on_upper_green(value):
    global u_green
    u_green[1] = value
    update_image()

# Callback function for the Hough threshold trackbar
def on_hough_threshold(value):
    global hough_threshold
    hough_threshold = value
    update_image()

# Create a named window for the trackbars
cv2.namedWindow("Adjust Green Threshold")

# Create trackbars for the lower and upper green values (0-255) with default values
initial_lower_green_value = 60  # Adjust this value as needed
initial_upper_green_value = 255  # Adjust this value as needed
initial_hough_threshold = 150  # Default Hough threshold value

cv2.createTrackbar("Lower Green Value", "Adjust Green Threshold", initial_lower_green_value, 255, on_lower_green)
cv2.createTrackbar("Upper Green Value", "Adjust Green Threshold", initial_upper_green_value, 255, on_upper_green)

# Create a trackbar for the Hough threshold value
cv2.createTrackbar("Hough Threshold", "Adjust Green Threshold", initial_hough_threshold, 500, on_hough_threshold)

# Read the image
frame = cv2.imread("OpenCV\greenscreen_grey.jpg")

# Calculate the maximum display size while maintaining the aspect ratio
max_width = 800
max_height = 600
aspect_ratio = frame.shape[1] / frame.shape[0]

if frame.shape[0] > max_height:
    frame = cv2.resize(frame, (int(max_height * aspect_ratio), max_height))
if frame.shape[1] > max_width:
    frame = cv2.resize(frame, (max_width, int(max_width / aspect_ratio)))

def hough_line_detection(frame):
    dst = cv2.Canny(frame, 50, 200, None, 3)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    
    lines = cv2.HoughLines(dst, 1, np.pi / 180, hough_threshold, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv2.line(cdst, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow("Hough Line Detection", cdst)

def update_image():
    global frame, u_green, l_green, hough_threshold
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

    # Perform Hough line detection
    hough_line_detection(result_image)

    # Continue with your existing code to replace red with transparency and display
    output_image = replace_red_with_transparency(result_image)
    cv2.imshow("Masked Image", output_image)

# Initial update
update_image()

while True:
    key = cv2.waitKey(10)
    if key == 27:
        break

cv2.destroyAllWindows()

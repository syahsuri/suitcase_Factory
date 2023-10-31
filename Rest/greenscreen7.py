# Imported libraries
import cv2 as cv
import numpy as np

# Declaration of variables
hough_threshold = 150

l_green = np.array([30, 30, 0])
u_green = np.array([104, 255, 104])

# Declare and import video/image material
frame = cv.imread("OpenCV\greenscreen_grey.jpg")

# Main code
def main():
    # Define global variables
    global frame, l_green, u_green, hough_threshold

    # Create a window for the adjustable trackbar
    open_modifier()


    #TEST





    # Apply post processing ---------

    # Create a mask for the background
    green_mask = cv.inRange(frame, l_green, u_green)
    cv.imshow("Green Mask #1", imgresize(green_mask))

    # Create a mask for the object in front of the background
    object_mask = cv.inRange(frame, np.array([0, 0, 0]), np.array([100, 100, 100]))
    cv.imshow("Object Mask #2", imgresize(object_mask))

    # Combine the green screen mask and the object mask
    mask = cv.bitwise_and(green_mask, cv.bitwise_not(object_mask))
    cv.imshow("Mask #3", imgresize(mask))

    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)

    # Dilate mask
    mask = cv.dilate(mask, kernel, iterations = 1)
    cv.imshow("Dilated Mask #4", imgresize(mask))

    # Erode mask
    mask = cv.erode(mask, kernel, iterations = 1)
    cv.imshow("Eroded Mask #5", imgresize(mask))

    # Combine mask with original frame
    frame_mask = cv.bitwise_and(frame, frame, mask = mask)
    cv.imshow("Mask #6", imgresize(frame_mask)) #Do We have to do this?

    # Create a red replacement for the green pixels
    red_pixels = np.zeros_like(frame)
    red_pixels[mask > 0] = [0, 0, 255]
    cv.imshow("Cut Out Area #7", imgresize(red_pixels)) #Do We have to do this?

    # Subtract the green-shaded pixels and add red pixels
    comb_frame = frame - frame_mask + red_pixels
    cv.imshow("Object On Cut Out #8", imgresize(comb_frame))

    # Continue with your existing code to replace red with transparency and display
    alpha_frame = alphanize(comb_frame)
    cv.imshow("Alpha Post Result #9", imgresize(alpha_frame))

    # Apply OpenCV algorhythms ---------

    # perform Canny edge detection
    canny_frame = canny_edge_detection(alpha_frame)
    cv.imshow("Canny Edge Result #10", imgresize(canny_frame))

    # Perform Hough line detection
    hough_frame = hough_line_detection(canny_frame)
    cv.imshow("Hough Line Result #11", imgresize(hough_frame))

    # Update
    update_image()




    cv.waitKey()
    cv.destroyAllWindows()

# Functions

# Resize display window
def imgresize(image):
    max_width = 800
    max_height = 600
    aspect_ratio = image.shape[1] / image.shape[0]

    if image.shape[0] > max_height:
        image = cv.resize(image, (int(max_height * aspect_ratio), max_height))
    if image.shape[1] > max_width:
        image = cv.resize(image, (max_width, int(max_width / aspect_ratio)))
    return image

# Upon changing the value of the lower green threshold
def on_lower_green(value):
    global l_green
    l_green[1] = value
    update_image()

# Upon changing the value of the lower green threshold
def on_upper_green(value):
    global u_green
    u_green[1] = value
    update_image()

# Callback function for the Hough threshold trackbar
def on_hough_threshold(value):
    global hough_threshold
    hough_threshold = value
    update_image()

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
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv.line(output_image, pt1, pt2, (0, 0, 255), 1, cv.LINE_AA)
    return output_image

def update_image():
    global frame, u_green, l_green, hough_threshold
    mask = cv.inRange(frame, l_green, u_green)
    
    # Create a mask for the object in front of the green screen
    object_mask = cv.inRange(frame, np.array([0, 0, 0]), np.array([100, 100, 100]))  # Adjust the threshold values for the object color
    
    # Combine the green screen mask and the object mask
    mask = cv.bitwise_and(mask, cv.bitwise_not(object_mask))
    
    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.dilate(mask, kernel, iterations=1)
    mask = cv.erode(mask, kernel, iterations=1)
    
    res = cv.bitwise_and(frame, frame, mask=mask)

    # Create a red replacement for the green pixels
    red_pixels = np.zeros_like(frame)
    red_pixels[mask > 0] = [0, 0, 255]

    # Subtract the green-shaded pixels and add red pixels
    result_image = frame - res + red_pixels

    output_image = alphanize(result_image)

    output_image = cv.GaussianBlur(output_image, (5, 5), 5)

    output_image = canny_edge_detection(output_image)
    # Perform Hough line detection
    output_image = hough_line_detection(output_image)

    # Continue with your existing code to replace red with transparency and display
    cv.imshow("Masked Image", imgresize(output_image))

def open_modifier():
    # Define global variables
    global l_green, u_green, hough_threshold

    # Name window
    cv.namedWindow("Modifier")

    # Create trackbars with default values
    initial_lower_green_value = 60  # Adjust this value as needed
    initial_upper_green_value = 255  # Adjust this value as needed
    initial_hough_threshold = 150  # Default Hough threshold value

    cv.createTrackbar("Minimum Green Value", "Modifier", initial_lower_green_value, 255, on_lower_green)
    cv.createTrackbar("Maximum Green Value", "Modifier", initial_upper_green_value, 255, on_upper_green)
    cv.createTrackbar("Hough Threshold", "Modifier", initial_hough_threshold, 500, on_hough_threshold)

main()
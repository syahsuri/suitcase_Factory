import cv2
import numpy as np

# Define a video capture object
vid = cv2.VideoCapture(0)

while True:
    # Capture the video frame by frame
    ret, frame = vid.read()

    # Check if a frame was successfully captured
    if ret:
        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the lower and upper thresholds for the green color
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([255, 255, 255])

        # Create a mask for the green color (background)
        background_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        # Invert the mask for the object (non-green areas)
        object_mask = cv2.bitwise_not(background_mask)

        # Create an all-black frame with the same size as the input frame
        black_background = np.zeros_like(frame)

        # Blend the original frame and the black background using the object mask
        result_frame = cv2.bitwise_and(frame, frame, mask=object_mask) + cv2.bitwise_and(black_background, black_background, mask=background_mask)

        # Display the original frame and the result
        cv2.imshow('Original Frame', frame)
    
        cv2.imshow('Result Frame', result_frame)
    #EDIT FRAME
    if ret:
        cv2.imshow('frame', frame)

    cv2.waitKey(200)
    #EDIT ^

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
vid.release()
cv2.destroyAllWindows()

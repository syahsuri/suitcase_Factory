import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale

def update_image(*args):
    global img1, img2, cvt1, cvt2
    threshold1 = threshold1_scale.get()
    threshold2 = threshold2_scale.get()

    bfilter = cv2.bilateralFilter(img1, 11, 17, 17)  # Noise reduction
    edged = cv2.Canny(bfilter, threshold1, threshold2)  # Edge detection
    cvt1 = cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)

    bfilter = cv2.bilateralFilter(img2, 11, 17, 17)  # Noise reduction
    edged = cv2.Canny(bfilter, threshold1, threshold2)  # Edge detection
    cvt2 = cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)

    Hori = np.concatenate((cvt1, cvt2), axis=1)
    cv2.imshow('Frame Test', Hori)

def on_closing():
    cv2.destroyAllWindows()
    root.quit()

root = tk.Tk()
root.title("Threshold Adjustment")

# Load images
img1 = cv2.imread('OpenCV/grey.png')
img2 = cv2.imread('OpenCV/black.png')

# Initial threshold values
initial_threshold1 = 10
initial_threshold2 = 300

# Threshold sliders
threshold1_scale = Scale(root, label="Threshold1", from_=0, to=500, orient="horizontal", length=300, command=update_image)
threshold1_scale.set(initial_threshold1)
threshold1_scale.pack()

threshold2_scale = Scale(root, label="Threshold2", from_=0, to=500, orient="horizontal", length=300, command=update_image)
threshold2_scale.set(initial_threshold2)
threshold2_scale.pack()

# Load and display the initial image
update_image()

# Close the OpenCV window properly
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

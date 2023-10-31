import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale
from matplotlib import pyplot as plt

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
    cv2.imshow('Edge Detection', Hori)

def threshold_images():
    global img, th1, th2, th3

    # Global thresholding
    ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Otsu's thresholding
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    images = [img, 0, th1,
              img, 0, th2,
              blur, 0, th3]
    titles = ['Original Noisy Image', 'Histogram', 'Global Thresholding (v=127)',
              'Original Noisy Image', 'Histogram', "Otsu's Thresholding",
              'Gaussian filtered Image', 'Histogram', "Otsu's Thresholding"]

    plt.figure(figsize=(10, 6))
    for i in range(3):
        plt.subplot(3, 3, i * 3 + 1), plt.imshow(images[i * 3], 'gray')
        plt.title(titles[i * 3]), plt.xticks([]), plt.yticks([])
        plt.subplot(3, 3, i * 3 + 2), plt.hist(images[i * 3].ravel(), 256)
        plt.title(titles[i * 3 + 1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3, 3, i * 3 + 3), plt.imshow(images[i * 3 + 2], 'gray')
        plt.title(titles[i * 3 + 2]), plt.xticks([]), plt.yticks([])

    plt.show()

def on_closing():
    cv2.destroyAllWindows()
    root.quit()

root = tk.Tk()
root.title("Threshold Adjustment")

# Load images
img1 = cv2.imread('OpenCV/grey.png')
img2 = cv2.imread('OpenCV/black.png')

img = cv2.imread('noisy2.png', 0)
th1 = th2 = th3 = None

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

# Threshold images button
threshold_button = tk.Button(root, text="Threshold Images", command=threshold_images)
threshold_button.pack()

# Close the OpenCV window properly
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

import cv2
from matplotlib import pyplot as plt
import numpy as np


img1 = cv2.imread('OpenCV/grey.png')
img2 = cv2.imread('OpenCV/black.png')

bfilter = cv2.bilateralFilter(img1, 11, 17, 17) #Noise reduction
edged = cv2.Canny(bfilter, 10, 300) #Edge detection
cvt1 = cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)

bfilter = cv2.bilateralFilter(img2, 11, 17, 17) #Noise reduction
edged = cv2.Canny(bfilter, 10, 300) #Edge detection
cvt2 = cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)

Hori = np.concatenate((cvt1, cvt2), axis=1)  
cv2.imshow('Frame Test', Hori)

cv2.waitKey(0)
cv2.destroyAllWindows()
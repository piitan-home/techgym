import os
import cv2
import matplotlib.pyplot as plt

os.chdir(os.path.abspath(__file__+'/../'))

img = cv2.imread('cat.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.imshow(img)
plt.show()
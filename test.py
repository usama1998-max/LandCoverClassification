import cv2
import numpy as np


filename = "162964_sat.jpg"

# load image as greyscale
img = cv2.imread(filename, 0)
#prev_img = cv2.imread(filename)

rimg = cv2.resize(img, (500, 500))
#primg = cv2.resize(prev_img, (500, 500))

#hsv_img = cv2.cvtColor(primg, cv2.COLOR_RGB2HSV)


# puts 0 to the white (background) and 255 in other places (greyscale value < 250)
# Threshold for river or sea
_, river_th = cv2.threshold(rimg, 200, 255, cv2.THRESH_BINARY_INV)
_, crop_th = cv2.threshold(rimg,  90, 100, cv2.THRESH_BINARY_INV)
_, vege_th1 = cv2.threshold(rimg, 80, 90, cv2.THRESH_BINARY_INV)


# # gets the labels and the amount of labels, label 0 is the background
_, label_river = cv2.connectedComponents(river_th)
_, label_crop = cv2.connectedComponents(crop_th)
_, label_vege1 = cv2.connectedComponents(vege_th1)


# # lets draw it for visualization purposes
preview1 = np.zeros((rimg.shape[0], rimg.shape[1], 3), dtype=np.uint8)

# # draw label 1 blue and label 2 green
preview1[label_river == 1] = (0, 0, 255)
preview1[label_crop == 0] = (0, 255, 0)
preview1[label_vege1 == 2] = (255, 0, 0)

cv2.imshow("frame1", preview1)
#cv2.imshow("original", primg)
# cv2.imshow("hsv", hsv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import numpy as np

# load image as greyscale
img = cv2.imread("main.jpg", 0)

prev_img = cv2.imread("main.jpg")

rimg = cv2.resize(img, (500, 500))
primg = cv2.resize(prev_img, (500, 500))

# puts 0 to the white (background) and 255 in other places (greyscale value < 250)
_, thresholded1 = cv2.threshold(rimg, 140, 255, cv2.THRESH_BINARY_INV)

# puts 0 to the white (background) and 255 in other places (greyscale value < 250)
_, thresholded2 = cv2.threshold(rimg, 150, 255, cv2.THRESH_TRIANGLE)

# gets the labels and the amount of labels, label 0 is the background
_, labels1 = cv2.connectedComponents(thresholded1)
_, labels2 = cv2.connectedComponents(thresholded2)


# lets draw it for visualization purposes
preview1 = np.zeros((rimg.shape[0], rimg.shape[1], 3), dtype=np.uint8)
preview2 = np.zeros((rimg.shape[0], rimg.shape[1], 3), dtype=np.uint8)

# draw label 1 blue and label 2 green
preview1[labels1 == 0] = (0, 255, 0)
preview2[labels2 == 0] = (0, 0, 255)


hsv_img = cv2.cvtColor(primg, cv2.COLOR_BGR2HSV)

lower_hsv = np.array([40, 150, 20])
higher_hsv = np.array([70, 255, 255])

mask = cv2.inRange(hsv_img, lower_hsv, higher_hsv)

# cv2.imshow("frame1", preview1)
# cv2.imshow("frame2", preview2)
cv2.imshow("hsv", hsv_img)
cv2.imshow("original", primg)
cv2.waitKey(0)
cv2.destroyAllWindows()

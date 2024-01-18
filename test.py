# import cv2
# import numpy as np
# from skimage.metrics import structural_similarity as ssim
#
# filename1 = "img_2017.jpg"
# filename2 = "img_2020.jpg"
#
#
# # Load two images from different time periods
# image1 = cv2.imread(filename1)
# image2 = cv2.imread(filename2)
#
# # Preprocess the images (e.g., resize, align, enhance)
#
# # Register the images (e.g., using feature-based registration)
# # Example: SIFT (Scale-Invariant Feature Transform)
# sift = cv2.SIFT.create()
#
# keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
# keypoints2, descriptors2 = sift.detectAndCompute(image2, None)
#
# # Match keypoints between the two images
# bf = cv2.BFMatcher()
# matches = bf.knnMatch(descriptors1, descriptors2, k=2)
#
# # Apply ratio test to filter good matches
# good_matches = []
# for m, n in matches:
#     if m.distance < 0.80 * n.distance:
#         good_matches.append(m)
#
# # Calculate the homography matrix to align the images
# if len(good_matches) > 4:
#     src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
#     dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
#     M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
#     result = cv2.warpPerspective(image1, M, (image2.shape[1], image2.shape[0]))
#
# # Perform change detection by subtracting the aligned images
# change_map = cv2.absdiff(result, image2)
#
# # Threshold and identify changes
# threshold = 30
# change_mask = cv2.threshold(change_map, threshold, 255, cv2.THRESH_BINARY)[1]
#
# # You can further process the change_mask to identify specific changes or areas of interest
# rimage1 = cv2.resize(change_mask, (500, 300))
#
# gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
# gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
#
# rgi1 = cv2.resize(gray_image1, (500, 300))
# rgi2 = cv2.resize(gray_image2, (500, 300))
#
# # Calculate SSIM score
# ssim_score = ssim(rgi1, rgi2)
#
# print(round(ssim_score, 2))
#
# # Display or save the change detection results
# cv2.imshow('Change Map', rimage1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# load image as greyscale
# img = cv2.imread(filename, 0)
#prev_img = cv2.imread(filename)

# rimg = cv2.resize(img, (500, 500))
#primg = cv2.resize(prev_img, (500, 500))

#hsv_img = cv2.cvtColor(primg, cv2.COLOR_RGB2HSV)


# puts 0 to the white (background) and 255 in other places (greyscale value < 250)
# Threshold for river or sea
# _, river_th = cv2.threshold(rimg, 200, 255, cv2.THRESH_BINARY_INV)
# _, crop_th = cv2.threshold(rimg,  90, 100, cv2.THRESH_BINARY_INV)
# _, vege_th1 = cv2.threshold(rimg, 80, 90, cv2.THRESH_BINARY_INV)


# # gets the labels and the amount of labels, label 0 is the background
# _, label_river = cv2.connectedComponents(river_th)
# _, label_crop = cv2.connectedComponents(crop_th)
# _, label_vege1 = cv2.connectedComponents(vege_th1)


# # lets draw it for visualization purposes
# preview1 = np.zeros((rimg.shape[0], rimg.shape[1], 3), dtype=np.uint8)

# # draw label 1 blue and label 2 green
# preview1[label_river == 1] = (0, 0, 255)
# preview1[label_crop == 0] = (0, 255, 0)
# preview1[label_vege1 == 2] = (255, 0, 0)

# cv2.imshow("frame1", preview1)
#cv2.imshow("original", primg)
# cv2.imshow("hsv", hsv_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
# import numpy as np
#
image = cv2.imread('6390_sat.jpg')
#
# rimg = cv2.resize(img, (250, 250), interpolation=cv2.INTER_AREA)
#
#
# blueChannel = rimg[:, :, 0]
# greenChannel = rimg[:, :, 1]
# redChannel = rimg[:, :, 2]
#
#
# c1_rgb = cv2.cvtColor(blueChannel, cv2.COLOR_GRAY2BGR)
# c2_rgb = cv2.cvtColor(greenChannel, cv2.COLOR_GRAY2BGR)
# c3_rgb = cv2.cvtColor(redChannel, cv2.COLOR_GRAY2BGR)
#
#
# stack1 = np.hstack([rimg, c1_rgb])
# stack2 = np.hstack([c2_rgb, c3_rgb])
# stack3 = np.vstack([stack1, stack2])
#


from skimage import feature, filters, measure

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

rimg = cv2.resize(gray_image, (500, 500), interpolation=cv2.INTER_AREA)

edged = cv2.Canny(rimg, 30, 200)


cv2.imshow("final image", edged)

cv2.waitKey(0)
cv2.destroyAllWindows()

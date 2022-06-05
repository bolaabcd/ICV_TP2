# Dado uma imagem, achar os alvos
import pygame
import cv2
import numpy as np
from pytest import approx

image = cv2.imread('1_frame.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
# alvo = cv2.imread('alvo.jpg')

# bw_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# gray = np.float32(bw_image)
# # bw_image = (image >= 128)*255

# edges = cv2.Canny(image,100,100)
# cv2.imshow('test.jpg',edges)
# cv2.waitKey()

# dst = cv2.cornerHarris(gray,2,3,0.04)
# #result is dilated for marking the corners, not important
# dst = cv2.dilate(dst,None)
# # Threshold for an optimal value, it may vary depending on the image.
# image[dst>0.01*dst.max()]=[0,0,255]

# cv2.imshow('test.jpg',image)
# cv2.waitKey()

# im = image.copy()
# imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# print(contours[1])
# cv2.drawContours(im, contours, 1, (0,255,0), 3)
# cv2.imshow('test.jpg',im)
# cv2.waitKey()

def area_rect_pixels(coords):
    assert(len(coords) == 4)
    p1,p2,p3,p4 = coords
    return abs(np.cross(p2-p1,p4-p1)/2)+abs(np.cross(p2-p3,p4-p3)/2)

tr2 = threshold.copy()
cv2.imshow('test.jpg',tr2)
contours, _ = cv2.findContours(tr2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

recs = []

for contour in contours:
    approx = cv2.approxPolyDP(
        contour, 0.01 * cv2.arcLength(contour, True), True)
  
    if len(approx) == 4 and approx[0][0][0] != 0 and area_rect_pixels(approx[:,0]) > 200:
        recs.append(approx[:,0])
        cv2.drawContours(image, [contour], 0, (0, 0, 255), 5)

print(recs)
  
# displaying the image after drawing contours
cv2.imshow('shapes', image)
  
cv2.waitKey()
cv2.destroyAllWindows()
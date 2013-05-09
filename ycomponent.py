'''
Created on May 9, 2013

@author: djordje
'''
import cv2


flnm = './test_pics/101.jpg'
img_bgr = cv2.imread(flnm, cv2.CV_LOAD_IMAGE_UNCHANGED)
img = cv2.cvtColor(img_bgr, cv2.cv.CV_BGR2YCrCb)
(img_y, x, y) = cv2.split(img)
cv2.imwrite('./test_pics/101_y.jpg', img_y)

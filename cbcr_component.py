'''
Created on Jun 14, 2013

@author: djordje
'''
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

def convert(path_to_in_dir, path_to_out_dir):
    """ Argument is the path to the directory containing images that will be 
        packed to the dictionary.
        
        Returns the dictionary containing image filename as label and
        image as value (image type is cvmat)."""
    files = [ filename
             for filename in listdir(path_to_in_dir)
             if isfile(join(path_to_in_dir,filename)) ]
    
    for flnm_raw in files:
        flnm = join(path_to_in_dir, flnm_raw)
        out_flnm = join(path_to_out_dir, flnm_raw)
        img_bgr = cv2.imread(flnm, cv2.CV_LOAD_IMAGE_UNCHANGED)
        img_ycrcb = cv2.cvtColor(img_bgr, cv2.cv.CV_BGR2HSV)
        
        H,W,_ = img_ycrcb.shape
        for h in xrange(H):
            for w in xrange(W):
                if not np.all(img_ycrcb[h,w] == np.array((255,128,128))):
                    img_ycrcb[h,w,0] = 180
        img_bgr_out = cv2.cvtColor(img_ycrcb, cv2.cv.CV_HSV2BGR)
        cv2.imwrite(out_flnm, img_bgr_out)


if __name__ == '__main__':
    convert('./test_colors/','./')
#! /usr/bin/python

import cv2
from os import listdir
from os.path import isfile, join
import parameters as P


def resize_(SCALE_TO, img_big, inflate=False):
    big_dim = max(img_big.shape)
    if big_dim > SCALE_TO:
        scale = SCALE_TO / float(big_dim)
    else:
        if inflate:
            scale = SCALE_TO / float(big_dim)
        else :
            scale = 1
    img = cv2.resize(img_big, (0, 0), fx=scale, fy=scale)
    return img

def get_dictionary(path_to_dir):
    """ Argument is the path to the directory containing images that will be 
        packed to the dictionary.
        
        Returns the dictionary containing image filename as label and
        image as value (image type is cvmat)."""
   
    SCALE_TO = P.parameters['scale_to_vertical_size']
    files = [ filename
             for filename in listdir(path_to_dir)
             if isfile(join(path_to_dir,filename)) ]
        
    print files
        
    idx_pic_dict = {}
    for flnm in files:
            
        str_idx = flnm
        str_idx = str_idx.partition('.')[0]
        flnm = join(path_to_dir, flnm)
            
        # Image creation
        img_bgr = cv2.imread(flnm, cv2.CV_LOAD_IMAGE_UNCHANGED)
        img_big = cv2.cvtColor(img_bgr, cv2.cv.CV_BGR2YCrCb)
        img = resize_(SCALE_TO, img_big)
        #Add img to the idx_pic_dict dictionary
        if (img == None): ## Check for invalid input
            print "Could not open or find the image"
        else:
            idx_pic_dict[str_idx] = img
    
    return idx_pic_dict

            
    
if __name__ == "__main__":
    pics_dict = get_dictionary("./test_pics")
    
    for k, v in pics_dict.iteritems():
        print v.shape
        cv2.namedWindow(k,2)
        cv2.resizeWindow(k, 800, 600)
        cv2.imshow(k, v)
        cv2.waitKey()


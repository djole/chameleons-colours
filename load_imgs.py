#! /usr/bin/python

import cv2
from os import listdir
from os.path import isfile, join

def get_dictionary(path_to_dir):
    """ Argument is the path to the directory containing images that will be 
        packed to the dictionary.
        
        Returns the dictionary containing image filename as label and
        image as value (image type is cvmat)."""
   

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
        img = cv2.cvtColor(img_bgr, cv2.cv.CV_BGR2YCrCb)
        
        #Add img to the idx_pic_dict dictionary
        if (img == None): ## Check for invalid input
            print "Could not open or find the image"
        else:
            idx_pic_dict[str_idx] = img
    
    return idx_pic_dict

            
    
if __name__ == "__main__":
    pics_dict = get_dictionary("./test_pics")
    
    """ Should be 001, 006, 020, 101, 101a as keys
        and: green face right cham., green face left cham., brown cham.,
        two white chams.
    """
    for k, v in pics_dict.iteritems():
        cv2.namedWindow(k,2)
        cv2.resizeWindow(k, 800, 600)
        cv2.imshow(k, v)
        cv2.waitKey()


import numpy as np
import unittest
from decimal import Decimal
from image_features import SpatialWordFeature
from parameters import parameters
import cv2
from numpy.core.numeric import dtype

WHITE_PADDING = 1
BLACK_PADDING = 2
FIXED_S_FEAT = 255

def get_image_pattern_words(image, word_cols,
                            word_rows=0, padding=WHITE_PADDING):
    """"""
    assert image.shape[2] == 3
    subsamp = 2
    
    if word_rows == 0:
        word_rows = word_cols
    
    image_cols = image.shape[1]
    image_rows = image.shape[0]
    num_word_cols = image_cols / word_cols
    num_word_rows = image_rows / word_rows
    words = []
    for w_r in xrange(num_word_rows):
        for w_c in xrange(num_word_cols):
            
            word_trans = (w_r*word_rows, w_c*word_cols)
            word_shape = (word_cols, word_rows)
            extract = get_subimage(image, word_shape, word_trans)
            # [channel, row, column]
            ''' channel[0] is Y component.
            Feature S is the mean of Y component.
            Feature P is the Y matrix normalized by S
            and represents the achromatic colour feature'''
            if not filter_word_with_padding(extract) : continue
            y_component = np.matrix(extract[0], dtype=extract.dtype)
            s_feat = y_component.mean()
            if Decimal(s_feat) != 0:
                p_feat = np.array(y_component.flatten() / s_feat)[0]
            else:
                p_feat = np.array(y_component.flatten() * s_feat)[0]
            
            ''' channels[1] & [2] represent the colour component.
            Feature C is the chromatic pattern fearure'''
            cb_component = np.matrix(extract[1], dtype=extract.dtype)
            cr_component = np.matrix(extract[2], dtype=extract.dtype)
            
            cb_subsampled = subsample_flatten_matrix(cb_component, subsamp)
            cr_subsampled = subsample_flatten_matrix(cr_component,subsamp)
            c_feat = np.concatenate((cb_subsampled, cr_subsampled), axis=0)
            
            if parameters['chrom_word_averaging']:
                if Decimal(s_feat) != 0 :
                    c_feat /= float(s_feat)
                else:
                    c_feat *= 0
            else:
                c_feat /= float(FIXED_S_FEAT)
            
            feature_word = SpatialWordFeature(p_feat, c_feat)
            words.append(feature_word)
    
    return words

def get_image_molecule_pattern_words(image, word_cols,
                            word_rows=0, padding=WHITE_PADDING):
    """"""
    assert image.shape[2] == 3
    
    if word_rows == 0:
        word_rows = word_cols
    
    imageBGR = cv2.cvtColor(image, cv2.cv.CV_YCrCb2BGR)
    imageHSV = cv2.cvtColor(imageBGR, cv2.cv.CV_BGR2HSV)
    image_cols = image.shape[1]
    image_rows = image.shape[0]
    num_word_cols = image_cols / word_cols
    num_word_rows = image_rows / word_rows
    words = []
    for w_r in xrange(num_word_rows):
        for w_c in xrange(num_word_cols):
            
            word_trans = (w_r*word_rows, w_c*word_cols)
            word_shape = (word_cols, word_rows)
            extract = get_subimage(imageHSV, word_shape, word_trans)
            extract = np.array(extract, dtype=np.uint8)
            # [channel, row, column]
            ''' channel[0] is Y component.
            Feature S is the mean of Y component.
            Feature P is the Y matrix normalized by S
            and represents the achromatic colour feature'''
            if not filter_word_with_padding(extract) : continue
            hue_component = np.array(extract[0], dtype=extract.dtype)
            red_conponent = hue_to_red(hue_component)
            yellow_component = hue_to_yellow(hue_component)
    
    return words

def hue_to_red(hue):
    pass

def hue_to_yellow(hue):
    pass

def subsample_element(in_matrix, row_idx, col_idx, subsample):
    output = 0.
    for i in range(subsample):
        for j in range(subsample):
            output += in_matrix[subsample*row_idx + i, subsample*col_idx + j]
    output /= subsample**2
    return output

def subsample_flatten_matrix(in_matrix, subsample):
    mat_shape = in_matrix.shape
    in_row = mat_shape[0]
    in_col = mat_shape[1]
    out_row = in_row/subsample
    out_col = in_col/subsample
    out_array = np.empty(out_row* out_col)
    for r in xrange(out_row):
        for c in xrange(out_col):
            sub_samp_val = subsample_element(in_matrix, r, c, subsample)
            flat_idx = r*out_col + c
            out_array[flat_idx] = sub_samp_val
    return out_array

def get_subimage(image, word_shape, word_trans):
    word_cols = word_shape[0]
    word_rows = word_shape[1]
    image_channels = image.shape[2]
    extract = np.zeros((image_channels, word_rows, word_cols))
    for pix_r in xrange(word_rows):
        for pix_c in xrange(word_cols):
            pixel = image[word_trans[0]+pix_r, word_trans[1]+pix_c]
            for ch in xrange(image_channels):
                extract[ch, pix_r, pix_c] = pixel[ch]

    return extract


def filter_word_with_padding(extract, allowed_padding=0.2,
                             padding=WHITE_PADDING, colorspace='YCrCb'):
    """ Returns a boolean value that tells if a bag of pixel values should pass the filter
    Parameters
    ----------
    extract : A 3D array of pixel values in YCbCr or HSV colour space
        Dimensions of the array are [channel (Y/H,Cb/S,Cr/V), row, column]
   
    Returns
    -------
    pass_ : boolean
        If the extract is part of the padding part of the image"""
    fst_elements = extract[0].flatten('C') # Y or H
    scnd_elements = extract[1].flatten('C') # Cb or S
    thrd_elements = extract[2].flatten('C') #Cr or V
    
    num_elements = extract.shape[1]*extract.shape[2]
    
    if padding == WHITE_PADDING : extreme = 255
    elif padding == BLACK_PADDING : extreme = 0
    
    if colorspace == 'YCrCb':
        fst_extreme = extreme
        scnd_extreme = 128
        thrd_extreme = 128
    elif colorspace == 'HSV':
        fst_extreme = 0
        scnd_extreme = 0
        thrd_extreme = extreme
    elif colorspace == 'RGB' or colorspace == "BGR":
        fst_extreme = extreme
        scnd_extreme = extreme
        thrd_extreme = extreme
    
    num_padds = 0
    for i in xrange(num_elements):
        if (fst_elements[i] == fst_extreme 
            and scnd_elements[i] == scnd_extreme
            and thrd_elements[i] == thrd_extreme):
                num_padds += 1
    
    if float(num_padds)/num_elements <= allowed_padding : 
        return True
    else : 
        return False

            
class word_tests(unittest.TestCase):
    
    def get_test_image(self):
        in_data = [[i, i+100, i+200] for i in xrange(100)]
        return np.array(in_data).reshape((20,5,3))
    
    def test_get_subimage_one(self):
        image = self.get_test_image()
        actual = get_subimage(image, (2,2), (5,1))
        exp_data = [26,27,31,32,126,127,131,132,226,227,231,232]
        expected = np.array(exp_data).reshape((3,2,2))
        self.assert_(image[5,1,0] == 26, "Input image not correct")
        self.assert_(np.array_equal(expected, actual),
                     "Image segment is not as expected")
        
    def test_get_pattern(self):
        parameters['chrom_word_averaging'] = True
        image = self.get_test_image()
        words = get_image_pattern_words(image, 2)
        actual_word_count = len(words)
        expected_word_count = 20
        self.assert_(actual_word_count == expected_word_count,
                     "Number of words failure")
    
    def test_subsample(self):
        mat = np.reshape(np.matrix(range(1,17)), (4,4))
        actual = subsample_flatten_matrix(mat, 2)
        s_feat = 0.5
        if Decimal(s_feat) != 0 :
            actual /= float(s_feat)
        else:
            actual *= 0
        expected = np.array([7, 11, 23, 27])
        self.assert_(np.array_equal(expected, actual),
                     "Subsampling method is not correct")
    
    def test_subsample_w2(self):
        mat = np.reshape(np.matrix(range(1,5)), (2,2))
        actual = subsample_flatten_matrix(mat, 2)
        s_feat = 0.5
        if Decimal(s_feat) != 0 :
            actual /= float(s_feat)
        else:
            actual *= 0
        expected = np.array([5])
        self.assert_(np.array_equal(expected, actual),
                     "Subsampling method is not correct")
    
    def test_subsample_noSubsamp(self):
        mat = np.reshape(np.matrix(range(1,5)), (2,2))
        actual = subsample_flatten_matrix(mat, 1)
        s_feat = 1
        if Decimal(s_feat) != 0 :
            actual /= float(s_feat)
        else:
            actual *= 0
        expected = np.array([1,2,3,4])
        self.assert_(np.array_equal(expected, actual),
                     "Subsampling method is not correct")
    
    def test_subsample_3Subsamp(self):
        mat = np.reshape(np.matrix(range(36)), (6,6))
        actual = subsample_flatten_matrix(mat, 3)
        s_feat = 1
        if Decimal(s_feat) != 0 :
            actual /= float(s_feat)
        else:
            actual *= 0
        expected = np.array([7,10,25,28])
        self.assert_(np.array_equal(expected, actual),
                     "Subsampling method is not correct")
if __name__ == '__main__':
    unittest.main()

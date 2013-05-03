import numpy as np
import unittest

WHITE_PADDING = 1
BLACK_PADDING = 2

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
            p_feat = np.array(y_component.flatten() / s_feat)[0]
            
            ''' channels[1] & [2] represent the colour component.
            Feature C is the chromatic pattern fearure'''
            cb_component = np.matrix(extract[1], dtype=extract.dtype)
            cr_component = np.matrix(extract[2], dtype=extract.dtype)
            
            cb_flat = np.array(cb_component.flatten())[0]
            cr_flat = np.array(cr_component.flatten())[0]
            
            cb_subsampled = np.array([s for (idx,s) in enumerate(cb_flat) 
                                        if idx%subsamp == 0])
            cr_subsampled = np.array([s for (idx,s) in enumerate(cr_flat) 
                                        if idx%subsamp == 0])
            c_feat = np.concatenate((cb_subsampled, cr_subsampled), axis=0)
            c_feat /= float(s_feat)
            
            feature_word = np.concatenate((p_feat, c_feat), axis=0)
            words.append(feature_word)
    
    return words

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
                             padding=WHITE_PADDING):
    """ Returns a boolean value that tells if a bag of pixel values should pass the filter
    Parameters
    ----------
    extract : A 3D array of pixel values in YCbCr colour space
        Dimensions of the array are [channel (Y,Cb,Cr), row, column]
   
    Returns
    -------
    pass_ : boolean
        If the extract is part of the padding part of the image"""
    
    y_elements = extract[0].flatten('C')
    cb_elements = extract[1].flatten('C')
    cr_elements = extract[2].flatten('C')
    
    num_elements = extract.shape[1]*extract.shape[2]
    
    if padding == WHITE_PADDING : extreme = 255
    elif padding == BLACK_PADDING : extreme = 0
    
    num_padds = 0
    for i in xrange(num_elements):
        if (y_elements[i] == extreme 
                    and cb_elements[i] == 128 and cr_elements[i] == 128):
            num_padds += 1
    
    if float(num_padds)/num_elements <= allowed_padding : 
        return True
    else : 
        return False
            
class work_tests(unittest.TestCase):
    
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
        image = self.get_test_image()
        words = get_image_pattern_words(image, 2)
        actual_word_count = len(words)
        expected_word_count = 20
        self.assert_(actual_word_count == expected_word_count,
                     "Number of words failure")

if __name__ == '__main__':
    unittest.main()

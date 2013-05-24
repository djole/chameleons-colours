'''
Created on May 7, 2013

@author: djordje
'''
import numpy as np
import unittest

class SpatialWordFeature(object):
    
    def __init__(self, achrom_word, chrom_word):
        self._achrom_word = achrom_word
        self._chrom_word = chrom_word
    
    def get_achrom_word(self):
        return self._achrom_word
    def get_chrom_word(self):
        return self._chrom_word

class SpatialWordHistogram(object):
    def __init__(self, hist_size):
        self._histogram = np.zeros(hist_size)
    
    def increment(self, index):
        self._histogram[index] += 1
    
    
    def __getitem__(self, idx):
        return self._histogram[idx]/self._histogram.sum()
    
    def __len__(self):
        return len(self._histogram)
        
def make_codebook_histogram(words_set, codebook):
    
    num_codes = len(codebook)
    code_histogram = SpatialWordHistogram(num_codes)
    for w_idx in xrange(len(words_set)):
        min_distance_code = 0
        min_distance = float('inf')
        for c_idx in xrange(num_codes):
            distance = (np.absolute(words_set[w_idx]-codebook[c_idx])).sum()
            if distance < min_distance:
                min_distance = distance
                min_distance_code = c_idx
        code_histogram.increment(min_distance_code)
        
    return code_histogram

class Tests(unittest.TestCase):
    def test_spatial_hist(self):
        self.assert_(len(SpatialWordHistogram(5)) == 5, "Hist size error")
if __name__ == '__main__':
    unittest.main()

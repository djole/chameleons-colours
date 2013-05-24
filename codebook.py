'''
Created on May 7, 2013

@author: djordje
'''
import numpy as np
import unittest

CODEBOOK_FSCL = 0


class Codebook(object):
    
    def __init__(self, num_words, word_size):
        self._codes = []
        for _ in xrange(num_words):
            ar = np.random.random_sample((word_size,))
            self._codes.append(ar)
    
    def __getitem__(self, idx):
        return self._codes[idx]
    
    def __setitem__(self, key, value):
        if not isinstance(value, np.ndarray):
            raise TypeError("value must be numpy.ndarray type")
        self._codes[key] = value
    
    def __len__(self):
        return len(self._codes)


class FSC_learning(object):

    @staticmethod
    def make_codebook(training_set, num_codes = 20,
                       train_iterations = 50, learn_fact = 0.1):
        # Initialize dimensions and codebooks
        
        some_word = training_set[0]
        word_size = len(some_word)
        word_count = len(training_set)
        word_hit_count = np.ones(num_codes)
        codebook = Codebook(num_codes, word_size)
        print "words to train on =", word_count
        for t_iter in xrange(train_iterations):
            print "training iter :", t_iter
            for w_iter in xrange(word_count):
                if w_iter % 10000 == 0: print w_iter,"/",word_count
                sample = training_set[w_iter]
                
                min_distance_code = 0
                min_distance = float('inf')
                for c_iter in xrange(num_codes):
                    distance = (np.absolute(codebook[c_iter] - sample)).sum()
                    distance *= word_hit_count[c_iter]
                    
                    if distance < min_distance:
                        min_distance = distance
                        min_distance_code = c_iter
                
                word_hit_count[min_distance_code] += 1
                win_code = codebook[min_distance_code]
                win_code += learn_fact * (sample - win_code)

        return codebook


def make_achrom_chrom_codebooks(words_dict):
    
    training_set_achrom = []
    training_set_chrom = []
    num_codes = 10
    num_train_iter = 1
    training_fact = 0.25
    
    for feats in words_dict.itervalues():
        for f in feats:
            training_set_achrom.append(f.get_achrom_word())
            training_set_chrom.append(f.get_chrom_word())
    
    print "Training achrom codebook"
    achrom_codebook = FSC_learning.make_codebook(training_set_achrom, num_codes,
                                                 num_train_iter, training_fact)
    
    print "Training chrom codebook"
    chrom_codebook = FSC_learning.make_codebook(training_set_chrom, num_codes,
                                                num_train_iter, training_fact)
    
    return (achrom_codebook, chrom_codebook)
    
    
    
'''Unit tests class'''
class FSCL_tests(unittest.TestCase):
    
    def test_make_codebook(self):
        word_zero = np.zeros(5)
        word_one = np.ones(5)
        training_set = [word_one, word_zero]
        codebook = FSC_learning.make_codebook(training_set, 2, 100, 0.25)
        diff_actual = (np.absolute(codebook[0]-codebook[1])).sum()
        diff_expected = 5
        self.assertAlmostEqual(diff_actual, diff_expected,
                               msg="Training incorrect", delta=0.001)

if __name__ == "__main__":
    unittest.main()
    
    

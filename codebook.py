'''
Created on May 7, 2013

@author: djordje
'''
import numpy as np


class Codebook:
    _words = []
    
    def __init__(self, num_words, word_size):
        
        for i in xrange(num_words):
            ar = np.random.random_sample((word_size,))
            self._words.append(ar)
    
    def __getitem__(self, idx):
        return self._words[idx]


def fsc_learning(training_set):
    
    # Initialize dimensions and codebooks
    number_of_words = 20
    some_word = training_set.values()[0][0]
    achrom_word_size = len(some_word.get_achrom_word())
    chrom_word_size = len(some_word.get_chrom_word())
    
    achrom_codebook = Codebook(number_of_words, achrom_word_size)
    chrom_codebook = Codebook(number_of_words, chrom_word_size)
    
    return (achrom_codebook, chrom_codebook)

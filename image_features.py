'''
Created on May 7, 2013

@author: djordje
'''

class SpatialWordFeature:
    _achrom_word = None
    _chrom_word = None
    
    def __init__(self, achrom_word, chrom_word):
        self._achrom_word = achrom_word
        self._chrom_word = chrom_word
    
    def get_achrom_word(self):
        return self._achrom_word
    def get_chrom_word(self):
        return self._chrom_word


'''
Created on May 21, 2013

@author: djordje
'''
from math import fabs
import unittest

class Euclidian_distance(object):
    '''Euclidian 2D distance'''
    def distance(self, point_a, point_b):
        return ((point_a[0]-point_b[0])**2. + (point_a[1]-point_b[1])**2.)**0.5

class Histograms_distance(object):
    
    def __init__(self, chrom_weight=1, achrom_weight=1):
        self._chrom_weight = chrom_weight
        self._achrom_weight = achrom_weight

    def distance(self, point_a, point_b):
        '''a point consists of a tuple where 1st member is achromatic hitogram
        and 2nd member is a chromatic histogram of that point'''
        hists_a = point_a
        hists_b = point_b
        
        achrom_hist_a = hists_a[0]
        achrom_hist_b = hists_b[0]
        
        chrom_hist_a = hists_a[1]
        chrom_hist_b = hists_b[1]
        
        achrom_diff = (self._achrom_weight *
                       self.histogram_diff(achrom_hist_a, achrom_hist_b))
        chrom_diff = (self._chrom_weight *
                      self.histogram_diff(chrom_hist_a, chrom_hist_b))
        return achrom_diff + chrom_diff
        
    
    def histogram_diff(self, hist_m, hist_n):
        if len(hist_m) != len(hist_n):
            raise PointDimensionError("Histograms sizes unequal")
        hist_diff_sum = 0
        for i in xrange(len(hist_m)):
            diff = fabs(hist_m[i] - hist_n[i])
            hist_diff_sum += diff/ (1 + hist_m[i] + hist_n[i])
        
        return hist_diff_sum

class PointDimensionError(Exception):
    def __init__(self, code=''):
        self._code = 'Points dimensionality mismatch: '+code
    
    def __str__(self):
        return repr(self._code)
    


class distance_tests(unittest.TestCase):
    def test_hist_distance(self):
        point_a = ([1,1,1],[1,1,1])
        point_b = ([2,2,2], [2,2,2])
        distance = Histograms_distance()
        actual_dist = distance.distance(point_a, point_b)
        expected_dist = 1.5
        self.assert_(actual_dist == expected_dist, "Distance error")
    
    def test_hist_size_exception(self):
        point_a = ([1,1,1],[1,1,1])
        point_b = ([2,2], [2,2,2])
        distance = Histograms_distance()
        try:
            distance.distance(point_a, point_b)
        except PointDimensionError, e:
            self.assert_(True, e.__str__())
            return
        self.assert_(False, "Should be an exception")
    
    def test_hist_distance_zero(self):
        point_a = ([0,0,0],[0,0,0])
        point_b = ([0,0,0], [0,0,0])
        distance = Histograms_distance()
        try:
            distance.distance(point_a, point_b)
        except:
            self.assert_(False, "Exception when zeroes")
            return
        self.assert_(True, "")  
        
    def test_hist_one(self):
        point_a = ([1,1,1])
        point_b = ([2,2,2])
        distance = Histograms_distance()
        try:
            distance.distance(point_a, point_b)
        except:
            self.assert_(True, "")
            return
        self.assert_(False, "Only one histogram exception not pressent")  

if __name__ == "__main__":
    unittest.main()
'''
Created on May 21, 2013

@author: djordje
'''
from abc import abstractmethod
from abc import ABCMeta
import unittest
from distance import Euclidian_distance

class Cluster_node(object):
    
    def __init__(self, label=None, left_child=None,
                  right_child=None, point=None):
        self._parent = None
        self._left_child = left_child
        self._right_child = right_child
        
        if left_child == None and right_child == None and point == None:
            raise InputArgumentsError(code="Must provide some input arguments")
        
        if bool(left_child) != bool(right_child): # XOR in Python
            er = "left_child and right_child have to both be either\
            None or not None"
            raise InputArgumentsError(code=er)
        if bool(label) != bool(point):
            er = "label and point have to both be either\
            None or not None"
            raise InputArgumentsError(code=er)
        if not((bool(left_child) or bool(right_child))
                != (bool(label) or bool(point))):
            er = "Cannot declare cluster node as both point\
                  cluster and set cluster"
            raise InputArgumentsError(code=er)
        
        if point == None:
            self._cluster_points = frozenset(left_child._cluster_points)
            self._cluster_points = (self._cluster_points.union
                                    (right_child._cluster_points))
            self._labels = frozenset(left_child._labels)
            self._labels = (self._labels.union
                            (right_child._labels))
            
        else:
            self._cluster_points = frozenset((point,))
            self._labels = frozenset((label,))
    
    def points(self):
        return self._cluster_points
    
    def labels(self):
        return self._labels
    
    def get_children(self):
        return (self._left_child, self._right_child)
    
    def get_newick_string(self):
        if self._left_child == None and self._right_child == None:
            return [n for n in self._labels][0]#Getting a value from a frozenset
        else:
            return ("(" + self._left_child.get_newick_string()
                    +"," + self._right_child.get_newick_string() + ")")

class Clustering(object):
    __metaclass__ = ABCMeta
    def __init__(self, distance):
        self._distance = distance
    
    def fit(self, points_dictionary):
        active_nodes = set([])
        
        for (k, v) in points_dictionary.iteritems():
            leaf = Cluster_node(label=k, point=v)
            active_nodes.add(leaf)
        
        while len(active_nodes) > 1:
            # loop until you reach the root of the cluster tree
            print "active nodes: ", len(active_nodes)
            closest_nodes = self.find_closest_nodes(active_nodes)
            new_node = Cluster_node(left_child=closest_nodes[0],
                                    right_child=closest_nodes[1])
            active_nodes.remove(closest_nodes[0])
            active_nodes.remove(closest_nodes[1])
            active_nodes.add(new_node)
        return active_nodes.pop()
    
    def find_closest_nodes(self, nodes_set):
        nodes_list = tuple(nodes_set)
        closest_nodes = None
        min_delta = float('inf')
        for i in xrange(len(nodes_list)):
            for j in xrange(i+1, len(nodes_list)):
                n1 = nodes_list[i]
                n2 = nodes_list[j]
                delta = self.nodes_difference(n1, n2)
                
                if delta < min_delta:
                    min_delta = delta
                    closest_nodes = (n1, n2)
        return closest_nodes
    
    @abstractmethod
    def nodes_difference(self, n1, n2):
        raise NotImplementedError()

class Complete_link_custering(Clustering):
    def __init__(self, distance):
        super(Complete_link_custering, self).__init__(distance)
    
    def nodes_difference(self, n1, n2):
        max_diff = 0.
        for pn1 in n1.points():
            for pn2 in n2.points():
                diff = self._distance.distance(pn1, pn2)
                if diff > max_diff:
                    max_diff = diff
        return max_diff
    
class Single_link_clustering(Clustering):
    def __init__(self, distance):
        super(Single_link_clustering, self).__init__(distance)
    
    def nodes_difference(self, n1, n2):
        min_diff = float('inf')
        for pn1 in n2.points():
            for pn2 in n2.points():
                diff = self._distance.distance(pn1, pn2)
                if diff < min_diff:
                    min_diff = diff
        return min_diff

class Average_link_clustering(Clustering):
    def __init__(self, distance):
        super(Average_link_clustering, self).__init__(distance)
        
    def nodes_difference(self, n1, n2):
        num_comparisons = len(n1.points()) * len(n2.points())
        sum_diff = 0.
        for pn1 in n1.points():
            for pn2 in n2.points():
                sum_diff += self._distance.distance(pn1, pn2)
        return sum_diff/num_comparisons
        
class InputArgumentsError(Exception):
    def __init__(self, code=None):
        self._code = code
    def __str__(self):
        s = "Invalid arguments: "
        return repr(s + self.code)


class Cluster_node_test(unittest.TestCase):
    def test_single_point(self):
        point_a = 1
        n1 = Cluster_node("a", left_child=None, right_child=None, point=point_a)
        expect_p = set((1,))
        expect_l = set(('a',))
        actual_p = n1.points()
        actual_l = n1.labels()
        self.assert_(expect_l==actual_l and expect_p==actual_p, "Value mismatch")
        
    def test_point_merge(self):
        point_a = 1
        point_b = 2
        n1 = Cluster_node(label='a', left_child=None,
                          right_child=None, point=point_a)
        n2 = Cluster_node(label='b', left_child=None,
                          right_child=None, point=point_b)
        n_m = Cluster_node(left_child=n1, right_child=n2)
        
        expect_p = set([1,2])
        expect_l = set(['a', 'b'])
        actual_p = n_m.points()
        actual_l = n_m.labels()
        
        is_same = actual_l == expect_l and actual_p == expect_p
        is_set = type(actual_p) == frozenset
        self.assert_(is_same and is_set, "Type or value mismatch")
    
    def test_cluster_merge(self):
        point_a = 1
        point_b = 2
        point_c = 3
        n1 = Cluster_node(label='a', left_child=None,
                          right_child=None, point=point_a)
        n2 = Cluster_node(label='b', left_child=None,
                          right_child=None, point=point_b)
        n_12 = Cluster_node(left_child=n1, right_child=n2)
        n3 = Cluster_node(label='c', left_child=None,
                          right_child=None, point=point_c)
        n_m = Cluster_node(left_child=n_12, right_child=n3)
        
        expect_p = set((1,2,3))
        expect_l = set(('a', 'b', 'c'))
        actual_p = n_m.points()
        actual_l = n_m.labels()
        
        is_same = actual_l == expect_l and actual_p == expect_p
        self.assert_(is_same, "Value mismatch")
    
    def test_newick_write(self):
        point_a = 1
        point_b = 2
        point_c = 3
        n1 = Cluster_node(label='a', left_child=None,
                          right_child=None, point=point_a)
        n2 = Cluster_node(label='b', left_child=None,
                          right_child=None, point=point_b)
        n_12 = Cluster_node(left_child=n1, right_child=n2)
        n3 = Cluster_node(label='c', left_child=None,
                          right_child=None, point=point_c)
        n_m = Cluster_node(left_child=n_12, right_child=n3)
        
        expected_tree = '((a,b),c)'
        actual_tree = n_m.get_newick_string()
        is_same = expected_tree == actual_tree
        error_print = "Newick tree incorrect: expected=" + expected_tree\
                       + ", actual tree=" + actual_tree
                    
        self.assert_(is_same, error_print)
    
    def one_exception_test(self, label, left_child,
                              right_child, point):
        try:
            Cluster_node(label=label, left_child=left_child,
                         right_child=right_child, point=point)
        except:
            return True
        return False
    
    def exception_args(self):
        point_a = 1
        point_b = 2
        n1 = Cluster_node(label='a', left_child=None,
                          right_child=None, point=point_a)
        n2 = Cluster_node(label='b', left_child=None,
                          right_child=None, point=point_b)
        
        return (point_a, point_b, n1, n2)
        
    def test_exception_1(self):
        (point_a, _, n1, _) = self.exception_args()
        test_pass = self.one_exception_test(label=None, left_child=None,
                                            right_child=n1, point=point_a)
        self.assert_(test_pass, "Exception not raised. test 1")
        
    def test_exception_2(self):
        (_, _, n1, n2) = self.exception_args()
        test_pass = self.one_exception_test(label='a', left_child=n1,
                                            right_child=n2, point=None)
        self.assert_(test_pass, "Exception not raised. test 2")
        
    def test_exception_3(self):
        (point_a, _, n1, n2) = self.exception_args()
        test_pass = self.one_exception_test(label=None, left_child=n1,
                                            right_child=n2, point=point_a)
        self.assert_(test_pass, "Exception not raised. test 3")
        
    def test_exception_4(self):
        (point_a, _, n1, n2) = self.exception_args()
        test_pass = self.one_exception_test(label='a', left_child=n1,
                                            right_child=n2, point=point_a)
        self.assert_(test_pass, "Exception not raised. test 4")
        
class Link_Clustering_tests(unittest.TestCase):
    

    def get_points(self):
        point_dict = {}
        point_dict["a"] = 1., 1.
        point_dict["b"] = 1.5, 1.
        point_dict["c"] = 3., 1.
        point_dict["d"] = 3., 2.
        point_dict["e"] = 2.5, 3.
        point_dict["f"] = 0.5, 1.5
        point_dict["g"] = 0.5, 2.
        return point_dict

    def test_fit_comlete(self):
        point_dict = self.get_points()
        
        distance = Euclidian_distance()
        clustering = Complete_link_custering(distance)
        root_n = clustering.fit(point_dict)
        (left_ch, right_ch) = root_n.get_children()
        expected_labels_left = set(['a','b','f','g'])
        actual_labels_left = left_ch.labels()
        actual_labels_right = right_ch.labels()
        
        is_correct = (expected_labels_left == actual_labels_left or 
                      expected_labels_left == actual_labels_right)
        assert(is_correct, 'Cluster partitioning incorrect')
        

if __name__ == '__main__':
    unittest.main()
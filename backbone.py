from words import get_image_pattern_words
import load_imgs
import codebook
import multiprocessing as mproc
import time
import image_features
import pickle
from hierarch_clustering import Complete_link_custering
from distance import Histograms_distance
import codeword_visuals as word_vis
import parameters as P

start_time = time.time()
window_size = P.parameters['window_size']

w_pool = mproc.Pool(processes = P.parameters['num_parallel'])

img_dict = load_imgs.get_dictionary(P.parameters['input_direct'])
print "img_dict ready!"

results = {}
for (k, img) in img_dict.iteritems() :
    results[k] = w_pool.apply_async(get_image_pattern_words,
                                    (img, window_size))
print "Jobs sent!"
words_dict = {}
num_tasks = len(results)

num_of_words = 0
for (k, res) in results.iteritems():
    words_dict[k] = results[k].get()
    num_of_words += len(words_dict[k])
    num_tasks -= 1
    print k, ". task collected,", len(words_dict[k]), "words in."
    print num_tasks, "tasks left"

print "Hello words!"
print num_of_words, "words in the bag"
print "exec time =", (time.time() - start_time)
(achrom_codebook, chrom_codebook) = \
    codebook.make_achrom_chrom_codebooks(
                                    words_dict,
                                    num_train_iter=P.parameters['train_iter'],
                                    num_codes=P.parameters['num_codewords'],
                                    training_fact=P.parameters['training_factor']
                                    )

histogram_dictionary = {}

for (k, v) in words_dict.iteritems():
    bag_achrom = []
    bag_chrom = []
    for w in v:
        bag_achrom.append(w.get_achrom_word())
        bag_chrom.append(w.get_chrom_word())
    
    print "making achrom histograms"
    achrom_hist = \
            image_features.make_codebook_histogram(bag_achrom,achrom_codebook)
    print "making chrom histograms"
    chrom_hist = \
            image_features.make_codebook_histogram(bag_chrom, chrom_codebook)
            
    histogram_dictionary[k] = (achrom_hist, chrom_hist)

distance = Histograms_distance(chrom_weight=P.parameters['chrom_hist_weight'],
                               achrom_weight=P.parameters['achrom_hist_weight'])
clustering = Complete_link_custering(distance)
print "start clustering"
top_node = clustering.fit(histogram_dictionary)


'''Saving the results'''
pickle_file = open("./top_node_save", 'w')
pickle.dump(top_node, pickle_file)
newick_file = open("./newick_tree.tre", 'w')
newick_file.write(top_node.get_newick_string())
word_vis.save_codewords(achrom_codebook,
                        word_vis.ACHROMATIC,
                        (window_size, window_size),
                        './'+P.parameters['achrom_codewords_name']+'.tiff')
word_vis.save_codewords(chrom_codebook,
                        word_vis.CHROMATIC,
                        (window_size, window_size),
                        './'+P.parameters['chrom_codewords_name']+'.tiff')

'''Making histograms' visualisation'''
for k,v in histogram_dictionary.iteritems():
    word_vis.draw_1histogram(histogram_dictionary[k][0], k, 'achrom')
    word_vis.draw_1histogram(histogram_dictionary[k][1], k, 'chrom')
    

print "the end"
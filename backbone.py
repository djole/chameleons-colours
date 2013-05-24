from words import get_image_pattern_words
import load_imgs
import codebook
import multiprocessing as mproc
import time
import image_features
import pickle
import gc
from hierarch_clustering import Complete_link_custering
from distance import Histograms_distance

start_time = time.time()
window_size = 10

w_pool = mproc.Pool(processes = 13)

img_dict = load_imgs.get_dictionary("/home/djordje/code/chameleons/Chameleon_segmented/")
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
    codebook.make_achrom_chrom_codebooks(words_dict,
                                         num_train_iter=100,
                                         num_codes=50,
                                         training_fact=0.1)

histogram_dictionary = {}

for (k, v) in words_dict.iteritems():
    bag_achrom = []
    bag_chrom = []
    for w in v:
        bag_achrom.append(w.get_achrom_word())
        bag_chrom.append(w.get_chrom_word())
    
    achrom_hist = \
            image_features.make_codebook_histogram(bag_achrom,achrom_codebook)
    chrom_hist = \
            image_features.make_codebook_histogram(bag_chrom, chrom_codebook)
            
    histogram_dictionary[k] = (achrom_hist, chrom_hist)

distance = Histograms_distance()
clustering = Complete_link_custering(distance)
top_node = clustering.fit(histogram_dictionary)

pickle_file = open("./top_node_save", 'w')
pickle.dump(top_node, pickle_file)
newick_file = open("./newick_tree.tre", 'w')
newick_file.write(top_node.get_newick_string())
words_dict = None
gc.collect()

# Init the codebooks
print "here"
from words import get_image_pattern_words
import load_imgs
import codebook
import multiprocessing as mproc
import time

start_time = time.time()
window_size = 4

w_pool = mproc.Pool(processes = 10, maxtasksperchild = 1)

img_dict = load_imgs.get_dictionary("./test_pics")
print "img_dict ready!"

results = {}
for (k, img) in img_dict.iteritems() :
    results[k] = w_pool.apply_async(get_image_pattern_words,
                                    (img, window_size))
print "Jobs sent!"
words_dict = {}
num_tasks = len(results)

num_of_words = 0
for (k, res) in results.iteritems() :
    words_dict[k] = results[k].get()
    num_of_words += len(words_dict[k])
    num_tasks -= 1
    print k, "task collected"
    print num_tasks, "tasks left"

print "Hello words!"
print num_of_words, "words in the bag"
print "exec time =", (time.time() - start_time)

# Init the codebooks
codebook.fsc_learning(words_dict)
print "here"
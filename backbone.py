from words import get_image_pattern_words
import load_imgs
import multiprocessing as mproc
import time

start_time = time.time()
window_size = 10

w_pool = mproc.Pool(processes = 5, maxtasksperchild = 2)

img_dict = load_imgs.get_dictionary("./test_pics/")
print "img_dict ready!"

results = {}
for (k, img) in img_dict.iteritems() :
    results[k] = w_pool.apply_async(get_image_pattern_words,
                                    (img, window_size))
print "Jobs sent!"
words_dict = {}
for (k, res) in results.iteritems() :
    words_dict[k] = results[k].get()
    print "Something's collected", k

print "Jobs collected!"
a_word_bag = words_dict['001']
print a_word_bag[34]
print "Hello words!"
print "exec time =", (time.time() - start_time)
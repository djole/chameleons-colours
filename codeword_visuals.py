'''
Created on May 24, 2013

@author: djordje
'''
from pylab import *
import parameters as P
import cv2
ACHROMATIC=0
CHROMATIC = 1
def codeword_as_img(code_word, word_shape, w_type,
                       show=False, save=False):
    #codeword is ndarray
    w_height = word_shape[0]
    w_length = word_shape[1]
    if w_type == ACHROMATIC:
        full_channel_img = np.ndarray((w_height, w_length, 1), dtype=np.uint8)
        code_mat = code_word.reshape(word_shape)
        for x in xrange(w_height):
            for y in xrange(w_length):
                val = int(round(code_mat[x,y]*128))
                full_channel_img[x,y] = val
    elif w_type == CHROMATIC:
        w_height /= 2
        w_length /= 2
        word_shape = (w_height, w_length)
        full_channel_img = np.ndarray((w_height, w_length, 3), dtype=np.uint8)
        word_ch1 = code_word[:(w_height*w_length)]
        word_ch2 = code_word[(w_height*w_length):]
        word_ch1 = word_ch1.reshape(word_shape)
        word_ch2 = word_ch2.reshape(word_shape)
        
        if P.parameters['chrom_word_averaging']: rescaling_factor = 128
        else: rescaling_factor = 255.
        
        for x in xrange(w_height):
            for y in xrange(w_length):
                val_cb = int(round(word_ch1[x,y]*rescaling_factor))
                val_cr = int(round(word_ch2[x,y]*rescaling_factor))
                full_channel_img[x,y] = [128, val_cb, val_cr]
                
        full_channel_img = cv2.cvtColor(full_channel_img, cv2.cv.CV_YCrCb2BGR)
    return full_channel_img

def show_codewords(code_dict, wtype, wshape):
    line = concatinate_all_imgs(code_dict, wtype, wshape)
    
    cv2.namedWindow("str(i)",2)
    cv2.resizeWindow("str(i)", 800, 600)
    cv2.imshow("str(i)", line)
    cv2.waitKey()
    

def concatinate_all_imgs(code_dict, wtype, wshape, straight=False):
    code_img = []
    for i in xrange(len(code_dict)):
        code_img.append(codeword_as_img(code_dict[i], wshape, wtype))
    if straight:
        line = reduce(lambda acc, el:
                      concatinate_2imgs(acc, el, place=1), code_img)
    else:
        line = glue_images(code_img)
    return line

def save_words(code_dict, wtype, wshape, filename, codewords=False):
    # Codewords are concatenated in straight line
    if codewords: strght = True
    else: strght = False
    line = concatinate_all_imgs(code_dict, wtype, wshape, straight=strght)
    
    if codewords:
        line = cv2.resize(line, (0,0), 
                          fx = 100, fy=100,
                          interpolation=cv2.INTER_NEAREST)
    
    cv2.imwrite(filename, line)

def glue_images(code_img):
    storage = []
    storage.append(list(code_img))
    storage.append([])
    switch = 0
    flip_it = lambda s: (s+1)%2
    
    while len(storage[switch]) > 1:
        # switch holds the index of the list that is currently
        # used as a storage for the results. It resonates between 0 and 1
        switch = flip_it(switch)
        n_imgs = len(storage[flip_it(switch)])
        for i in xrange(0, n_imgs, 2):
            if i+1 < n_imgs:
                img1 = storage[flip_it(switch)][i]
                img2 = storage[flip_it(switch)][i+1]
                storage[switch].append(concatinate_2imgs(img1, img2, switch))
            else:
                img_ = storage[flip_it(switch)][i]
                storage[switch].append(img_)
        storage[flip_it(switch)] = []
    bucket = storage[switch][0]
#    bucket = cv2.resize(bucket, (0,0), fx = 2,
#                        fy=2, interpolation=cv2.INTER_NEAREST)
    return bucket

def concatinate_2imgs(img1, img2, place=0):
    ''' place == 0 means that images will be concatenated horizontally,
        place == 1 means that images will be concatenated vertically'''
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    if place == 0:
        h = max(h1, h2)
        w = w1+w2
    elif place == 1:
        h = h1 + h2
        w = max(w1, w2)

    if len(img1.shape) == 3 :
        ch = img1.shape[2]
        vis = np.zeros((h, w, ch), np.uint8)
    else:
        vis = np.zeros((h, w), np.uint8)
        
    if place == 0:
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1+w2] = img2
    elif place == 1:
        vis[:h1, :w1] = img1
        vis[h1:h1+h2, :w2] = img2
    return vis
    
def draw_1histogram(histogram, label, glabel=''):
    n = len(histogram)
    X = np.arange(n)
    bar(X, histogram, facecolor='blue', edgecolor='black', label=label)
    xlim(0, n)
    #legend(loc='upper left')
    xticks(xrange(n))
    savefig(P.parameters['histograms_dict']+label+glabel+'.png',dpi=72)
    close()
    
    
if __name__ == '__main__':
    bag = []
    for i in xrange(900):
        bag.append(np.zeros((1,1), np.uint8) + 255)
    m = glue_images(bag)
    m = cv2.resize(m, (0,0), fx = 100, fy=100, interpolation=cv2.INTER_NEAREST)
    cv2.imwrite('./words/test_concat.png', m)
    
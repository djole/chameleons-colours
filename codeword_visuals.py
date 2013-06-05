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
        for x in xrange(w_height):
            for y in xrange(w_length):
                val_cb = int(round(word_ch1[x,y]*128))
                val_cr = int(round(word_ch2[x,y]*128))
                full_channel_img[x,y] = [128, val_cb, val_cr]
                
        full_channel_img = cv2.cvtColor(full_channel_img, cv2.cv.CV_BGR2YCrCb)
#    full_channel_img = cv2.resize(full_channel_img, (0,0), fx=10, fy=10)
    return full_channel_img

def show_codewords(code_dict, wtype, wshape):
    line = concatinate_all_imgs(code_dict, wtype, wshape)
    
    cv2.namedWindow("str(i)",2)
    cv2.resizeWindow("str(i)", 800, 600)
    cv2.imshow("str(i)", line)
    cv2.waitKey()
    

def concatinate_all_imgs(code_dict, wtype, wshape):
    code_img = []
    for i in xrange(len(code_dict)):
        code_img.append(codeword_as_img(code_dict[i], wshape, wtype))
    
    line = reduce(lambda acc, el:concatinate_2imgs(acc, el), code_img)
    return line

def save_codewords(code_dict, wtype, wshape, filename):
    line = concatinate_all_imgs(code_dict, wtype, wshape)
    cv2.imwrite(filename, line)
    

def concatinate_2imgs(img1, img2):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    if len(img1.shape) == 3 :
        ch = img1.shape[2]
        vis = np.zeros((max(h1, h2), w1+w2, ch), np.uint8)
    else:
        vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1+w2] = img2
    return vis

def draw_codeword_histograms(hist_dict):
    for (k,v) in hist_dict.iter_items():
        pass
    
def draw_1histogram(histogram, label, glabel=''):
    n = len(histogram)
    X = np.arange(n)
    bar(X, histogram, facecolor='blue', edgecolor='black', label=label)
    xlim(0, n)
    #legend(loc='upper left')
    xticks(xrange(n))
    savefig(P.parameters['histograms_dict']+label+glabel+'.png',dpi=72)
    close()
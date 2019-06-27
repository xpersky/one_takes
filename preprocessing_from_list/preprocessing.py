import os
import sys

stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

from fastai.core import parallel
import multiprocessing as mp
import numpy as np

from keras.preprocessing.image import load_img, save_img, img_to_array
sys.stderr = stderr

tarr = ["{}".format(i) for i in os.listdir()]
tsiz = (200,200)
tdir = 'test'
    
def preProcess(value,index):
    name,size,directory,target = value
    try:
        if target == '--resize':
            im = img_to_array(load_img(name,target_size=size))
        elif target == '--random crop':
            img = img_to_array(load_img(name))
            assert img.shape[2] == 3 
            height, width = img.shape[0], img.shape[1]
            dx, dy = size
            if height > dy and width > dx: 
                x = np.random.randint(0, width - dx + 1)
                y = np.random.randint(0, height - dy + 1)
                im = img[y:(y+dy),x:(x+dx), :]
            else:
                im = img           
        path = directory + '/' + name
        save_img(path,im)
        return 1 # status ok
    except:
        return 0 # status bad

def preprocess_parallel(arr,size,directory,target):
    args = [ (name,size,directory,target) for name in arr]
    status = parallel(preProcess,args)
    if status == len(arr):
        print("STATUS_CODE == OK")
    else:
        print("STATUS_CODE == NOT ALL FILES COULD BE LOADED {}/{}".format(sum(status),len(arr)))
    

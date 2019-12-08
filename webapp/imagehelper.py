# Jose I Retamal
# Emerging Technologies 
# GMIT 2019
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import base64 as b64
from collections import deque

"""
 Provide some helper methods for prepare images containig numbers for use in a model
 trained using Mnist dataset.
"""


def cropImage(image, limit):
    """
    Crop a grey color with no tranparency  image from all sides.
    Must be a 2D array
    : param limit : value of pixel for crop. 
    : return :  croped image.
    """
    # crop top-bot
    x, y = image.shape
    topLimit = 0
    ib = 0  # use for break the outer loop
    for i in range(0, x):
        for j in range(0, y):
            if(image[i][j] == limit):
                ib = 1
        if ib == 1:
            break
        topLimit += 1

    # will crop with 1 padding
    if topLimit > 0:
        topLimit -= 1
    # crop image
    image = np.delete(image, range(0, topLimit), 0)

    # crop left-right
    # get new shape
    x, y = image.shape
    # crop right-left
    ib = 0  # for break outer loop
    leftLimit = 0

    for i in range(0, y):
        for j in range(0, x):
            # colum contain the limit we break
            if(image[j][i] == limit):
                ib = 1
        if ib == 1:
            break
        leftLimit += 1

    # crop with 1 padding
    if leftLimit > 0:
        leftLimit -= 1
    # crop
    image = np.delete(image, range(0, leftLimit), 1)

    # crot bot-top
    # get new shape
    x, y = image.shape
    ib = 0  # use for break outer loop
    bottomLimit = 0
    for i in range(x-1, 0, -1):
        for j in range(y-1, 0, -1):
            if(image[i][j] == limit):
                ib = 1
        if ib == 1:
            break
        bottomLimit += 1

    # crop with 1 padding
    if bottomLimit > 0:
        bottomLimit -= 1
    image = np.delete(image, range(x-bottomLimit, x), 0)

    # crop right-left
    # get new shape
    x, y = image.shape
    ib = 0
    rightLimit = 0
    for i in range(y-1, 0, -1):
        for j in range(x-1, 0, -1):
            if(image[j][i] == limit):
                ib = 1
        if ib == 1:
            break
        rightLimit += 1

    if rightLimit > 0:
        rightLimit -= 1
    image = np.delete(image, range(y-rightLimit, y), 1)

    return image, rightLimit, leftLimit, topLimit, bottomLimit


def cropRL(image, limit):
    """
    Crop image only from Right to left.
    : param limit : value of pixel for crop. 
    : return :  croped image.
    """
    # crop right-left
    # get new shape
    x, y = image.shape
    ib = 0
    rightLimit = 0
    for i in range(y-1, 0, -1):
        for j in range(x-1, 0, -1):
            if(image[j][i] == limit):
                ib = 1
        if ib == 1:
            break
        rightLimit += 1

    if rightLimit > 0:
        rightLimit -= 1

    image = np.delete(image, range(y-rightLimit, y), 1)

    return image, rightLimit


def converTo1D(img, w, h):

    a = np.asarray(img)

    n = []
    for number in a:
        for j in number:
            n.append(j[1])
    # convert to 2d np array
    return np.array(n).reshape(w, h)


def divedeQueue(iq):
    """
    Separate in idividual number a queue that contain images, images must be 
    the sequence of writing the number from left to right. Please see for explanatin.
    : param iq :  queue containing the sequence of images. 
    : return :  queue containig each separate number as 2d array.
    """
    rs = deque([]) #queue for put indidual number images(results)
    
    img_x_limit = 0 # 
    img_x_limit_last = 0 
    rn = 0
    is_first_img = True
    count = 0

    ## process first image outside loop
    img = iq.popleft() 
    w, h = img.size
    img = converTo1D(img, h, w)
    img_r, r = cropRL(img, 255)
    rs.append(img_r)
        
    img_x_Limit = w-r
    remain = None # overlap
    remain2 = None
    img_n = None

    while len(iq) is not 0:
        img = iq.popleft() #get image from queue
        w, h = img.size # get actual img size 
        # get right and left side of img limited by img_x_limit
        img_l = img.crop((img_x_limit_last, 0, img_x_Limit, h)) 
        img_r = img.crop((img_x_Limit, 0, w, h))
        # get both img sizes
        wr, hr = img_r.size
        wl, hl = img_l.size
        img_l = converTo1D(img_l, hl, wl)# convter into 1d np array
        # check if there is overlap and remove it if there is
        if remain2 is not None:
            h2, w2 = remain2.shape
            img_l = img_l - np.delete(remain2, range(wl, w2), 1)
            remain2 = None
        img_r = converTo1D(img_r, hr, wr)# convert into 1D array
        #check if there is a new number or anothe line of the old
        isNew = np.array_equal(img_l, rs[len(rs)-1])
        if isNew == False: # if is not new number remplace last
            rs.pop()
            rs.append(img_l)
            remain = img_r
        else: # if is new number we add to result queue
            if remain is not None:
                img_r = img_r - remain
                remain2 = remain
                remain = None
            img_n, r = cropRL(img_r, 255)
            img_x_limit_last = img_x_Limit
            img_x_Limit = img_x_Limit + wr - r
            rs.append(img_n)
        is_first_img = False# for check when is firt img in
    return rs


def simulateMnist(img):
    """
    Resize a image for simulate a Mnist image.
    Will resize the image to 20x20, calcualte pixels center of mass and then
    place image into a 28x28 image with the center of mass at the center.
    : param img :  image to simulate. 
    : return : 28x28 2D array containg the number.
    """
  
    i, j = img.shape
    img = Image.fromarray(img)

    ish = i > j  # scale horizontal if true
    w, h = 200, 200
    # want to keep scale at 10 multiplied
    if ish:
        img = img.resize(((int(round((int(round(w/10))/i)*j))*10), h))
    else:
        img = img.resize((w, (int(round((int(round(h/10))/j)*i))*10)))
    img = np.asarray(img)

    # fill for 200x200 image
    x, y = img.shape
    if ish:
        res = w-y
        p = np.zeros((h, int(res/2)), dtype=np.int)
        img = np.concatenate((p, img), axis=1)
        img = np.concatenate((img, p), axis=1)
    else:
        res = h-x
        p = np.zeros((int(res/2), w), dtype=np.int)
        img = np.concatenate((p, img), axis=0)
        img = np.concatenate((img, p), axis=0)

    # scale to 20x20 simulating
    f = []
    sum = 0
    for i0 in range(0, w, 10):
        for j0 in range(0, h, 10):
            sum = 0
            for i in range(i0, i0+10):
                for j in range(j0, j0+10):
                    if img[i][j] == 0:
                        sum += 1
            if sum == 0:
                sum = 0.01  # we don't want 0 because Mnist has not 0
            f.append((sum)/100)

    f = np.array(f).reshape(int(w/10), int(h/10))

    # calculate pixel center of mass
    ii, jj = f.shape
    totaly, totalx = 0, 0
    cy, cx = 0, 0
    for i in range(0, ii):
        for j in range(0, jj):
            if f[i][j] != 0:
                totaly += (i)
                cy += 1
            if f[i][j] != 0:
                totalx += (j)
                cx += 1
    cx, cy = int(round(totalx/cx)), int(round(totaly/cy))

    # fill image top
    top = np.ones((14-cy, 20), dtype=np.int)
    f = np.concatenate((top, f), axis=0)

    # fill bot
    bot = np.ones((28-((14-cy)+20), 20), dtype=np.int)
    f = np.concatenate((f, bot), axis=0)

    # fill left
    left = np.ones((28, 14-cx), dtype=np.int)
    f = np.concatenate((left, f), axis=1)
    
    # fill right
    right = np.ones((28, 28-((14-cx)+20)),
                    dtype=np.int)  # (28-((14-cx)+20)
    f = np.concatenate((f, right), axis=1)
   
    return f




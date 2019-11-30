import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import base64 as b64
from collections import deque


def cropImage(image, limit):
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
    rs = deque([])
    img = iq.popleft()
    w, h = img.size
    img = converTo1D(img, h, w)
    img_r, r = cropRL(img, 255)
    rs.append(img_r)
    start = 0
    rn = 0
    isFirst = True

    count = 0
    oldstart = 0
    start = w-r
    remain = None
    remain2 = None
    img_n = None

    while len(iq) is not 0:

        img = iq.popleft()
        # iq.append(img)
        w, h = img.size

        img_l = img.crop((oldstart, 0, start, h))

        img_r = img.crop((start, 0, w, h))
        wr, hr = img_r.size
        wl, hl = img_l.size
        img_l = converTo1D(img_l, hl, wl)
        if remain2 is not None:
            h2, w2 = remain2.shape
            img_l = img_l - np.delete(remain2, range(wl, w2), 1)
            remain2 = None
        img_r = converTo1D(img_r, hr, wr)

        isNew = np.array_equal(img_l, rs[len(rs)-1])
     
        if isNew == False:
            rs.pop()
            rs.append(img_l)
            remain = img_r
        else:
            if remain is not None:
                img_r = img_r - remain
                remain2 = remain
                remain = None
            img_n, r = cropRL(img_r, 255)
            oldstart = start
            start = start + wr - r
            rs.append(img_n)
    # if(count == 4):
        #   break
        #count += 1
        isFirst = False

    return rs


def simulateMnist(img):
  
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

    top = np.ones((14-cy, 20), dtype=np.int)
    f = np.concatenate((top, f), axis=0)

    bot = np.ones((28-((14-cy)+20), 20), dtype=np.int)
    f = np.concatenate((f, bot), axis=0)

    left = np.ones((28, 14-cx), dtype=np.int)
    f = np.concatenate((left, f), axis=1)
    right = np.ones((28, 28-((14-cx)+20)),
                    dtype=np.int)  # (28-((14-cx)+20)
    f = np.concatenate((f, right), axis=1)

   
    return f


# img = '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'
# img = Image.open(BytesIO(b64.b64decode(img))).convert('LA')


# img = np.asarray(img)
# n = []
# for number in img:
#     for j in number:
#         n.append(j[1])

# img = np.array(n)
# img = img.reshape(200, 800)
# img,r,l,t,b = cropImage(img, 255)

# plt.imshow(img, cmap='gray')
# plt.show()

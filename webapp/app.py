# modified from : https://palletsprojects.com/p/flask/
import flask as fl
from flask import escape, request
from keras.models import load_model
import numpy as np
import json
from flask_cors import CORS
# xxxxxxxxxxxxxxx
import tensorflow as tf
import gzip
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
import sys
import logging
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#from keras.layers import Dense, Dropout, Flatten
import concurrent.futures
import urllib.request
import base64 as b64
from PIL import Image
from io import BytesIO
import re
import pandas as pd
import imagearray 
from collections import deque

# logging.basicConfig(level=logging.DEBUG)

app = fl.Flask(__name__)
CORS(app)
# app.run(host="127.0.0.1",port=5000,threaded=False)

# import the model
tf.keras.backend.set_learning_phase(0)  # Ignore dropout at inference
model = load_model('../models/model73.h5')

img_queue = deque([])

# Add index route
@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route("/imgs", methods=["POST", "GET"])
def add_img():

    if request.method == "POST":
        # get data from request
        image64 = request.data.decode("utf-8")
        
        # remove header
        data = re.sub('data:image/png;base64,', '', image64)
        print(data)
        # open image as grayscale
        img = Image.open(BytesIO(b64.b64decode(data))).convert('LA')
        img_queue.append(img)
        print(len(img_queue))

        return "added"
    if request.method == "GET":
        print("Hello")
        #first image
        rs = imagearray.divedeQueue(img_queue)
        print(len(rs))

        while True:
            if(len(rs)==0):
                 break
            img = rs.popleft()
            img,x1,x2,x4,x4 = imagearray.cropImage(img,255)
            img = imagearray.simulateMnist(img)
            print(img.shape)
            #plt.imshow(img, cmap='gray')
            #plt.savefig("img.png")
            img = img.reshape(1,28,28,1)
            result = model.predict(img)
            print(result)
            high = 0
            num = 0
            pos = 0
            for x in result[0]:
                if x > high:
                    high = x
                    num = pos
                pos += 1
            print(num)
        return "7"


@app.route("/clear", methods=["POST"])
def clear_img():
    if request.method == "POST":
        clearImages()
        print(len(img_queue))
        return "true"


@app.route("/reco", methods=["GET", "POST"])
def process():

    if request.method == "POST":

        # get data from request
        image64 = request.data.decode("utf-8")
        # remove header
        data = re.sub('data:image/png;base64,', '', image64)
        # open image as grayscale
        img = Image.open(BytesIO(b64.b64decode(data))).convert('LA')
        img_queue.append(img)
        print(len(img_queue))
        # original size
        w, h = 200, 800

        # convert to array with 1 int
        # doing just Image.open(BytesIO(b64.b64decode(data))).convert('L') don't work becuase image has a transparent chanel
        # https://stackoverflow.com/questions/44997339/convert-python-image-to-single-channel-from-rgb-using-pil-or-scipy
        a = np.asarray(img)
        n = []
        for number in a:
            for j in number:
                n.append(j[1])
        # convert to 2d np array
        n = np.array(n).reshape(w, h)
        n, r, l, t, b = imagearray.cropImage(n, 255)

       # plt.imshow(n, cmap='gray')

        # scale image to width or height
        img = Image.fromarray(n)

        i, j = n.shape
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
                f.append((sum/100.0))#.astype('float32')

        f = np.array(f).reshape(int(w/10), int(h/10))

        #print(f.shape)
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

       # print(f)
        f = f.reshape(1, 28, 28, 1)
        # make prediction
        result = model.predict(f)

        print(result)

        high = 0
        num = 0
        pos = 0
        for x in result[0]:
            if x > high:
                high = x
                num = pos
            pos += 1
        print(num)

    return str(num)


def make_prediction(img):
    model = load_model('../models/cnn.h5')
    result = model.predict(img)
    return result


def clearImages():
    img_queue.clear()


if __name__ == '__main__':
    app.run(debug=True)

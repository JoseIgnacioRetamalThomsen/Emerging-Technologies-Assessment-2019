# modified from : https://palletsprojects.com/p/flask/
import flask as fl
from flask import escape, request
from keras.models import load_model
import numpy as np
import json
from flask_cors import CORS
import tensorflow as tf
import sys
import logging
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# import concurrent.futures
import urllib.request
import base64 as b64
from PIL import Image
from io import BytesIO
import re
import imagehelper as ih
from collections import deque

#flask run --host=0.0.0.0 --port=80

app = fl.Flask(__name__)
CORS(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
# app.run(host='0.0.0.0',port=5001)

# import the model
tf.keras.backend.set_learning_phase(0)  # Ignore dropout at interface
# model = load_model('../model/model7.h5')
model = load_model('../model/static/model.h5')
model.summary()

# images queue
img_queue = deque([])

# Add index route
@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route("/imgs", methods=["POST", "GET"])
def add_img():
    # add images to queue
    if request.method == "POST":
        # get data from request
        imgs = deque([])
        y = json.loads(request.data)
        for x in y:
            image64 = x#.decode("utf-8")
            # remove header
            data = re.sub('data:image/png;base64,', '', image64)
            # open image as grayscale
            img = Image.open(BytesIO(b64.b64decode(data))).convert('LA')
            # add image to queue
            imgs.append(img)
        rs = ih.divedeQueue(imgs)
        numb =""
        # loop rs which contain individual images
        while True:
            # end loop if queue empty
            if(len(rs)==0):
                 break
            # get first image
            img = rs.popleft()
            # crop image
            img,x1,x2,x4,x4 = ih.cropImage(img,255)
            # add simulated raster and put image in pixel center of amss 
            img = ih.simulateMnist(img)
            # reshape for use in model
            img = img.reshape(1,28,28,1)
            # predict actual number
            result = model.predict(img)
            # get value from result vector
            num = np.argmax(result, axis=-1)[0]
            # add actual number to result
            numb+= str(num)
        return numb
        
    # process images
    if request.method == "GET":
        # separate images in individual numbers 
        rs = ih.divedeQueue(img_queue)
        # for create result
        numb =""
        # loop rs which contain individual images
        while True:
            # end loop if queue empty
            if(len(rs)==0):
                 break
            # get first image
            img = rs.popleft()
            # crop image
            img,x1,x2,x4,x4 = ih.cropImage(img,255)
            # add simulated raster and put image in pixel center of amss 
            img = ih.simulateMnist(img)
            # reshape for use in model
            img = img.reshape(1,28,28,1)
            # predict actual number
            result = model.predict(img)
            # get value from result vector
            num = np.argmax(result, axis=-1)[0]
            # add actual number to result
            numb+= str(num)
        return numb

# creal images queue 
@app.route("/clear", methods=["POST"])
def clear_img():
    if request.method == "POST":
        clearImages()
      
        return "true"

# def make_prediction(img):
#     model = load_model('../models/cnn.h5')
#     result = model.predict(img)
#     return result

def clearImages():
    img_queue.clear()

# if __name__ == '__main__':
#     app.run(host="192.168.43.57")

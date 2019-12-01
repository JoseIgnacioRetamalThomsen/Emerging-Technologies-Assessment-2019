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
import concurrent.futures
import urllib.request
import base64 as b64
from PIL import Image
from io import BytesIO
import re
import imagehelper as ih 
from collections import deque

# 

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

    # add images to queue
    if request.method == "POST":
        # get data from request
        image64 = request.data.decode("utf-8")
        # remove header
        data = re.sub('data:image/png;base64,', '', image64)
        # open image as grayscale
        img = Image.open(BytesIO(b64.b64decode(data))).convert('LA')
        # add image to queue
        img_queue.append(img)
        return "OK"

    if request.method == "GET":
       
        #first image
        rs = ih.divedeQueue(img_queue)
        numb =""
        while True:
            if(len(rs)==0):
                 break
            img = rs.popleft()
            img,x1,x2,x4,x4 = ih.cropImage(img,255)
            img = ih.simulateMnist(img)
            img = img.reshape(1,28,28,1)
            result = model.predict(img)
            num = np.argmax(result, axis=-1)[0]
            numb+= str(num)
     
        return numb


@app.route("/clear", methods=["POST"])
def clear_img():
    if request.method == "POST":
        clearImages()
      
        return "true"

def make_prediction(img):
    model = load_model('../models/cnn.h5')
    result = model.predict(img)
    return result


def clearImages():
    img_queue.clear()


if __name__ == '__main__':
    app.run(debug=True)

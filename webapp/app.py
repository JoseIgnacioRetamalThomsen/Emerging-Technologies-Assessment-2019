# Jose I Retamal
# Emerging Technologies 
# GMIT 2019

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
import urllib.request
import base64 as b64
from PIL import Image
from io import BytesIO
import re
import imagehelper as ih
from collections import deque

app = fl.Flask(__name__)
CORS(app)

# import the model
tf.keras.backend.set_learning_phase(0)  # Ignore dropout at interface
model = load_model('../model/static/model.h5')

# Add index route
@app.route('/')
def home():
    """
    Main route return static index.
    """
    return app.send_static_file('index.html')

@app.route("/imgs", methods=["POST", "GET"])
def predict():
    """
    Main end point get, get a array of images in json format 
    Responde wiht a json array compose by predictions.
    """
  
    if request.method == "POST":
        try:
            #Parse request into a list of images
            imgs = processRequestData(request.data)
            # Create single number images from list
            rs = ih.divedeQueue(imgs)
            # Make a prediction for each single image
            prediction = predictFromQueue(rs)
            # Response json list
            return json.dumps(prediction)
        except:
            return  "Not posible to process request", 400


#############
# Utilities #
#############

def processRequestData(jsonRequest):
    """
    Process request from client.
    Request is a json array with pictures,
    Parse pictures and append them into a queue.
    :param jsonRequest: Json binary request.
    :return: queue with images.
    """
    imgs = deque([])
    y = json.loads(jsonRequest)
    for x in y:
        image64 = x#.decode("utf-8")
        # remove header
        data = re.sub('data:image/png;base64,', '', image64)
        # open image as grayscale
        img = Image.open(BytesIO(b64.b64decode(data))).convert('LA')
        # add image to queue
        imgs.append(img)
    return imgs

def predictFromQueue(imgQueue):
    """
    Generate preditions from a list of images.
    :param imgQueue: List of images.
    :return: list with prediction, first element in the list is all predictions on a strins.
    """
    response = []
    response.append("")
    numb =""
    while True:
        # end loop if queue empty
        if(len(imgQueue)==0):
                break
        # get first image
        img = imgQueue.popleft()
        # crop image
        img,x1,x2,x4,x4 = ih.cropImage(img,255)
        # add simulated raster and put image in pixel center of amss 
        img = ih.simulateMnist(img)
        # reshape for use in model
        img = img.reshape(1,28,28,1)
        # predict actual number
        result = model.predict(img)
        response.append(result.tolist())
        # get value from result vector
        num = np.argmax(result, axis=-1)[0]
        # add actual number to result
        numb+= str(num)
    response[0] = numb
    return response

 

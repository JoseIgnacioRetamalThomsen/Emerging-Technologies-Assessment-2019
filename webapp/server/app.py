#modified from : https://palletsprojects.com/p/flask/
import flask as fl
from flask import  escape, request
from keras.models import load_model
import numpy as np
import json
from flask_cors import CORS
#xxxxxxxxxxxxxxx
import tensorflow as tf
import gzip
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
import sys
import logging
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from keras.layers import Dense, Dropout, Flatten
import concurrent.futures
import urllib.request

#logging.basicConfig(level=logging.DEBUG)

app = fl.Flask(__name__)
CORS(app)
#app.run(host="127.0.0.1",port=5000,threaded=False)

#import the model
# Ignore dropout at inference
tf.keras.backend.set_learning_phase(0)
model = load_model('../../models/55_33_22_124_10_9941.h5')

@app.route("/reco", methods=["GET", "POST"])
def process():

    
    #global graph
   # graph = tf.get_default_graph()
  

    if request.method == "POST": 
        
        #get data from request then convert it into a  28x28 np array
        image = np.array(json.loads(request.data))
        
        image = np.array(image)
        image = image.reshape(1,28,28,1)
        #image = image.reshape(28,28)
        #finalImg = finalImg.astype('float32')
        
        finalImg = image/255
       

        # reshape image
        #finalImg  = ~np.array(list(image)).reshape(1, 784).astype(np.uint8) / 255.0
        #finalImg = np.reshape(1, 784)

        # make prediction
        result = model.predict(image) 
  
        high =0
        num =0
        pos = 0
        for x in result[0]:
            if x > high:
                high = x
                num = pos
            pos +=1
        print(num)

        # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        #     future = executor.submit(make_prediction,finalImg)
        #     print(future.result())

    return f'Hello, !'


def make_prediction(img):
    model = load_model('../models/cnn.h5')
    result = model.predict(img)
    return result


if __name__ == '__main__':
    app.run(debug=True)



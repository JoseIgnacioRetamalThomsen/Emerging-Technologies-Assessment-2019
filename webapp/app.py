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
import base64 as b64
from PIL import Image 
from io import BytesIO
import re
import pandas as pd

#logging.basicConfig(level=logging.DEBUG)

app = fl.Flask(__name__)
CORS(app)
#app.run(host="127.0.0.1",port=5000,threaded=False)

#import the model
# Ignore dropout at inference
tf.keras.backend.set_learning_phase(0)
model = load_model('../models/model73.h5')

@app.route("/reco", methods=["GET", "POST"])
def process():

    
    #global graph
   # graph = tf.get_default_graph()
  

    if request.method == "POST":

        image64 = request.data.decode("utf-8") 
        data = re.sub('data:image/png;base64,', '',image64)
        print(data)
        image = Image.open(BytesIO(b64.b64decode(data))).convert('LA')
        img = image.resize((20,20))
        
        img.show()
        print(image)
        a = np.asarray(img)
        n = []
        for number in a:
            for j in number:
                n.append(j[1])
        n = np.array(n)
        n = n.reshape(20,20)
        plt.imshow(n, cmap='gray')
        plt.show()
        img.save("test.png")
        mask = n>0
        n =a[np.ix_(mask.any(1),mask.any(0))]
        print(n)
        #Image.fromarray(a,"RGB").show()
       # print(image)
    #     c = 0
    #     for i in image:
    #         image[c] = 255-i
    #         c += 1
    #     print(image)
    #     image = np.array(image)
    #     image = image.reshape(1,28,28,1)
    #     image = image.astype('float32')
    #     image /= 255
    #     count =0
        
      
    #     #image = image.reshape(28,28)
    #     #finalImg = finalImg.astype('float32')
    #   # print(image)
    #     finalImg = image
       

    #     # reshape image
    #     #finalImg  = ~np.array(list(image)).reshape(1, 784).astype(np.uint8) / 255.0
    #     #finalImg = np.reshape(1, 784)

    #     # make prediction
    #     result = model.predict(image) 
  
    #     high =0
    #     num =0
    #     pos = 0
    #     for x in result[0]:
    #         if x > high:
    #             high = x
    #             num = pos
    #         pos +=1
    #     print(num)

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



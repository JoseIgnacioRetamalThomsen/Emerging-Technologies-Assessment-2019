#modified from : https://palletsprojects.com/p/flask/
import gzip
import numpy as np
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
from keras.models import load_model
from flask import  escape, request
import flask as fl
import sys
import logging
import json
from flask_cors import CORS
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from keras.layers import Dense, Dropout, Flatten
import concurrent.futures
import urllib.request

#logging.basicConfig(level=logging.DEBUG)

app = fl.Flask(__name__)
CORS(app)
#app.run(host="127.0.0.1",port=5000,threaded=False)

model = load_model('./models/CRAZY.h5')


@app.route("/reco", methods=["GET", "POST"])
def process():

 
   #global graph
    #graph = tf.get_default_graph()


    if request.method == "POST": 
        
        #get data from request then convert it into a  28x28 np array
        image = np.array(json.loads(request.data))
                 
        # reshape image
        finalImg  = ~np.array(list(image)).reshape(1, 784).astype(np.uint8) / 255.0
        #finalImg = np.reshape(1, 784)

        # make prediction
        result = model.predict(finalImg) 
  
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
    model = load_model('./models/t1.h5')
    result = model.predict(img)
    return result


if __name__ == '__main__':
    app.run(debug=True)




#modified from : https://palletsprojects.com/p/flask/
import gzip
import numpy as np
import keras as kr
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
from keras.models import load_model
from flask import  escape, request
import flask as fl
import sys
import logging
import json
from flask_cors import CORS

#logging.basicConfig(level=logging.DEBUG)

app = fl.Flask(__name__)
CORS(app)

model = load_model('../model/first.h5')

@app.route("/reco", methods=["GET", "POST"])
def process():


 
    
    
    if request.method == "POST": 
        f = open("demofile2.txt", "a")   
        data = json.loads(request.data)
        
        image = []
        i =0
        j =0
        for key in data:
            for mx in key:
                image.append(mx)
                print(f'{i} {j}')
                j += 1
            i += 1
            j=0
        #print(data)
        f.write("tet")#data.get('name'))
    
        print(image)
        finalImg  = ~np.array(list(image)).reshape(1, 784).astype(np.uint8) / 255.0
       
        print(finalImg)
        result = model.predict(finalImg)
        print(result)
    
    return f'Hello, !'

 
if __name__ == '__main__':
    app.run(debug=True)
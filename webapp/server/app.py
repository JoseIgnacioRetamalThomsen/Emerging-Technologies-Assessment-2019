
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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

#logging.basicConfig(level=logging.DEBUG)

app = fl.Flask(__name__)
CORS(app)

model = load_model('./models/first.h5')

@app.route("/reco", methods=["GET", "POST"])
def process():


 
    
    
    if request.method == "POST": 
        
        data = json.loads(request.data)
        
        image = []
        i =0
        j =0
        for key in data:
            for mx in key:
                image.append(mx)
                
                j += 1
            i += 1
            j=0
        #print(data)
        f = open("demofile0.txt", "a")
        for i in image:
            f.write(f'{str(i)} ')
        f.close()
      #  plt.imshow(image, cmap='gray')
        ##print(image)
        finalImg  = ~np.array(list(image)).reshape(1, 784).astype(np.uint8) / 255.0
        ii=0

        for nn in finalImg[0]:
            if nn == 1 :
                print(" %s " % "0", end="", flush=True)
            else:
                print(" %s " % "x", end="", flush=True)
            ii += 1
            if ii == 28:
                print()
                ii=0
        
        plt.imshow(finalImg, cmap='gray')
     
      #  plt.show()
        result = model.predict(finalImg)
      #  print(result)
        high =0
        num =0
        pos = 0
        for x in result[0]:
            if x > high:
                high = x
                num = pos
            pos +=1
        print(num)


    return f'Hello, !'

 
if __name__ == '__main__':
    app.run(debug=True)
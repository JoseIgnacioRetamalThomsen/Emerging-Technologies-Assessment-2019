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
tf.keras.backend.set_learning_phase(0) # Ignore dropout at inference
model = load_model('../models/model73.h5')

# Add index route
@app.route('/')
def home():
  return app.send_static_file('index.html')

@app.route("/reco", methods=["GET", "POST"])
def process():

    
    #global graph
   # graph = tf.get_default_graph()
  

    if request.method == "POST":

        image64 = request.data.decode("utf-8") 
        data = re.sub('data:image/png;base64,', '',image64)
        print(data)
        img = Image.open(BytesIO(b64.b64decode(data))).convert('LA')
        #img = image.resize((20,20))
        
        # PROCESS IMAGE
        w,h = 200,800
        # convert to array with 1 int
        a = np.asarray(img)
        n = []
        for number in a:
            for j in number:
                n.append(j[1])
        n = np.array(n)
        n = n.reshape(w,h)
        n = cropImage(n,255)
      #  x,y = n.shape


        # # crop left right
        # count = 0
        # ib = 0
        # for i in range(0,x):
        #     for j in range(0,y):
        #         if(n[i][j]==255):
        #             ib = 1
        #     if ib==1:
        #         break
        #     count +=1

        # if count >0:
        #     count -= 1
        # n = np.delete(n, range(0,count), 0)

        # x,y = n.shape
        # # crop right-left
        # ib=0
        # count2 =0
        # for i in range(0,y):
        #     for j in range(0,x):
        #         if(n[j][i]==255):
        #             ib=1
        #     if ib==1:
        #         break
        #     count2+=1
        
        # n = np.delete(n, range(0,count2), 1)

        # #crot top-bot
        # x,y = n.shape

        # ib=0
        # count3 =0
        # for i in range(x-1,0,-1):
        #     for j in range(y-1,0,-1):
        #         if(n[i][j]==255):
        #             ib=1
        #     if ib==1:
        #         break
        #     count3+=1

        # n = np.delete(n, range(x-count3,x), 0)

        # # crop bot-top
        # x,y = n.shape
        # ib=0
        # count4 =0
        # for i in range(y-1,0,-1):
        #     for j in range(x-1,0,-1):
        #         if(n[j][i]==255):
        #             ib=1
        #     if ib==1:
        #         break
        #     count4+=1
        
        # n = np.delete(n, range(y-count4,y), 1)

        plt.imshow(n, cmap='gray')
        
        img = Image.fromarray(n)
        #img.show()
     
        i,j = n.shape
        ish = i>j
        w,h = 200,200
        if ish:
            img = img.resize( ((int(round((int(round(w/10))/i)*j))*10) ,h))
        else:
            img = img.resize( (w,(int(round((int(round(h/10))/j)*i))*10)))
        
        img = np.asarray(img)
        x,y =img.shape
        if ish:
            res = w-y
            p = np.zeros((h, int(res/2)), dtype = np.int)
            img = np.concatenate((p, img), axis = 1)
            img = np.concatenate((img,p),axis =1)
        else:
            res = h-x
            p = np.zeros((int(res/2),w), dtype = np.int)
            img = np.concatenate((p, img), axis = 0)
            img = np.concatenate((img,p),axis =0)

        f = []
        sum =0
        for i0 in range(0,w,10):
            for j0 in range(0,h,10):
                sum=0
                for i in range (i0,i0+10):
                    for j in range (j0,j0+10):
                        if img[i][j]==0:
                            sum +=1
                f.append(1 -((100-sum)/100))
        
        f = np.array(f)

        f = f.reshape(int(w/10),int(h/10))

        print(f.shape)

        ii,jj = f.shape
        totaly, totalx = 0 , 0
        cy,cx = 0 , 0 
        for i in range(0,ii):
            for j in range(0,jj):
                if f[i][j]!=0:
                    totaly += (i)
                    cy+=1
                if f[i][j]!=0:
                    totalx += (j)
                    cx+=1
        cx,cy = int(round(totalx/cx)),int(round(totaly/cy))

        top = np.ones((14-cy, 20), dtype = np.int)
        f = np.concatenate((top, f), axis = 0)

        bot = np.ones((28-((14-cy)+20), 20), dtype = np.int)
        f = np.concatenate((f, bot), axis = 0)

        left = np.ones((28, 14-cx), dtype = np.int)
        f = np.concatenate((left, f), axis = 1)
        right = np.ones((28,28-((14-cx)+20)), dtype = np.int)#(28-((14-cx)+20)
        f = np.concatenate((f, right), axis = 1)

       # print(f)
        f = f.reshape(1,28,28,1)
        #make prediction
        result = model.predict(f) 

        print(result)

        high =0
        num =0
        pos = 0
        for x in result[0]:
            if x > high:
                high = x
                num = pos
            pos +=1
        print(num)
    
    return str(num)

def make_prediction(img):
    model = load_model('../models/cnn.h5')
    result = model.predict(img)
    return result


if __name__ == '__main__':
    app.run(debug=True)



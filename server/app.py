
#modified from : https://palletsprojects.com/p/flask/
import gzip
import numpy as np
import keras as kr
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
from keras.models import load_model
from flask import Flask, escape, request

app = Flask(__name__)

model = load_model('../model/first.h5')

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

    ### setup
    #  py -3 -m venv venv

    # venv\Scripts\activate 
    # pip instal flask
 
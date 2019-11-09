import gzip
import numpy as np
import keras as kr
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Flatten

model = load_model('./models/CRAZY.h5')

(x_train, y_train), (x_test, y_test) = mnist.load_data()

inputs = ~np.array(x_train).reshape(60000,784)/255.0
inputs = inputs.astype('float32')


test_inputs =  ~np.array(x_test).reshape(10000,784)/255.0
test_inputs = test_inputs.astype('float32')

y_test = y_test.astype('float32')
encoder = pre.LabelBinarizer()
encoder.fit(y_test)
test_outputs = encoder.transform(y_test)

scores = model.evaluate(test_inputs, test_outputs, verbose=0)

print(scores)
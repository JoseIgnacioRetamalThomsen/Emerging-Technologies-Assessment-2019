import gzip
import numpy as np
import keras as kr
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Flatten

(x_train, y_train), (x_test, y_test) = mnist.load_data()

inputs = ~np.array(x_train).reshape(60000,784)/255.0

inputs = inputs.astype('float32')


model = kr.models.Sequential()

#model.add(kr.layers.Dense(units=1568, activation='relu',input_dim=784))
model.add(kr.layers.Dense(units=784, activation='relu'))
#model.add(Dropout(0.01))
model.add(kr.layers.Dense(units=392, activation='relu'))
#model.add(Dropout(0.005))
model.add(kr.layers.Dense(units=98, activation='relu'))
#model.add(kr.layers.Dense(units=30, activation='relu'))
model.add(kr.layers.Dense(units=10, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

y_train = y_train.astype('float32')
encoder = pre.LabelBinarizer()
encoder.fit(y_train)
outputs = encoder.transform(y_train)

model.fit(inputs, outputs, epochs=100, batch_size=100)


test_inputs =  ~np.array(x_test).reshape(10000,784)/255.0
test_inputs = test_inputs.astype('float32')

y_test = y_test.astype('float32')
encoder = pre.LabelBinarizer()
encoder.fit(y_test)
test_outputs = encoder.transform(y_test)

#model.save("784-392-98-10-nd.h5")

scores = model.evaluate(test_inputs, test_outputs, verbose=0)

print(scores)
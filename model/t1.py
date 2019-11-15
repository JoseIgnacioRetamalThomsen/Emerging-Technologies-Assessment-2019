import gzip
import numpy as np
import keras as kr
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Flatten
from keras import regularizers
import matplotlib.pyplot as plt
from keras.layers.normalization import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K

model = load_model('./model11.h5')


(x_train, y_train), (x_test, y_test) = mnist.load_data()

#print(x_train[0])
#inputs = ~np.array(x_train).reshape(60000,784)/255.0
#inputs = inputs.astype('float32')

# create 28 by 28 arrays
# x_train = x_train.reshape(x_train.shape[0], 1, 28, 28)
# x_test = x_test.reshape(x_test.shape[0],1,28,28)
# https://github.com/yashk2810/MNIST-Keras/blob/master/Notebook/MNIST_keras_CNN-99.55%25.ipynb
# input_shape = (1, 28, 28)
img_rows=28
img_cols=28
num_classes =10

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
    print("This")
else:
    x_train = ~x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = ~x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)
    print("other")

#print("Before")
#print(x_train[0])

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
#print(x_train[0])
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

y_train = kr.utils.to_categorical(y_train, num_classes)
y_test = kr.utils.to_categorical(y_test, num_classes)

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
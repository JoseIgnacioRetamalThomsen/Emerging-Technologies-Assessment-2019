import gzip
import numpy as np
import keras as kr
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Flatten
from keras import regularizers
#
from keras import backend as K

(x_train, y_train), (x_test, y_test) = mnist.load_data()

inputs = ~np.array(x_train).reshape(60000,784)/255.0
inputs = inputs.astype('float32')

# create 28 by 28 arrays
# x_train = x_train.reshape(x_train.shape[0], 1, 28, 28)
# x_test = x_test.reshape(x_test.shape[0],1,28,28)

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


x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = kr.utils.to_categorical(y_train, num_classes)
y_test = kr.utils.to_categorical(y_test, num_classes)


model = kr.models.Sequential()
model.add(kr.layers.Conv2D(32,kernel_size=(7, 7),
                 activation='relu',
                 input_shape=(28,28,1)))

model.add(kr.layers.Conv2D(64,kernel_size=(5, 5),activation='relu'))
model.add(kr.layers.Conv2D(128,kernel_size=(3, 3),activation='relu'))
#model.add(kr.layers.Conv2D(256,kernel_size=(3, 3),activation='relu'))
#model.add(kr.layers.Conv2D(128, (2, 2), activation='relu'))
model.add(kr.layers.MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
#model.add(Dropout(0.4))

#model.add(kr.layers.Dense(units=84, activation='relu'))
#model.add(Dropout(0.2))

model.add(Dropout(0.5))
model.add(kr.layers.Dense(units=10, activation='softmax'))

model.compile(loss=kr.losses.categorical_crossentropy,optimizer='adadelta',metrics=['accuracy'])

#model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

#model.fit(x_train, x_test, epochs=10, batch_size=128)


history_callback = model.fit(x_train, y_train,
          batch_size=128,
          epochs=2 ,
          verbose=1,
          validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)

# accuracy on test data
val_accuracy = np.array(history_callback.history['val_accuracy'])
# loss on test data
val_loss =  np.array(history_callback.history['val_loss'])

#on train data
accuracy =  np.array(history_callback.history['accuracy'])
loss =  np.array(history_callback.history['loss'])


print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save("cll.h5")
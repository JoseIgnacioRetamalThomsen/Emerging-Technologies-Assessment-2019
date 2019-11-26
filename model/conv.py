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
#
from keras import backend as K

#https://stackoverflow.com/questions/55371645/is-there-a-way-to-save-a-model-at-a-specified-epoch-in-tf-keras
class CustomModelCheckpoint(kr.callbacks.Callback):
    minimun = 0.99
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    def init(self):
        self.x_test = ~self.x_test.reshape(self.x_test.shape[0], img_rows, img_cols, 1)
        self.x_test = self.x_test.astype('float32')
        self.x_test /= 255
        self.y_test = kr.utils.to_categorical(y_test, num_classes)

    def on_epoch_end(self, epoch, logs=None):
        score = self.model.evaluate(x_test, y_test, verbose=0)
        # logs is a dictionary
        print(f"epoch: {epoch},history_callback.{logs['val_accuracy']}")
        print(score[1])
        if score[1] > self.minimun: # your custom condition
    
            self.model.save('model11.h5', overwrite=True)
           
            print("saved")
            
           
            
            self.minimun = score[1]
            print(self.minimun)


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


x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
#print(x_train[0])
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = kr.utils.to_categorical(y_train, num_classes)
y_test = kr.utils.to_categorical(y_test, num_classes)
print(x_train[0])
model = kr.models.Sequential()

# model.add(kr.layers.Conv2D(64,kernel_size=(7, 7),activation='relu',input_shape=(28,28,1)))
# BatchNormalization(axis=-1)
# model.add(Dropout(0.05))
# model.add(kr.layers.Conv2D(128,kernel_size=(7, 7),activation='relu'))
# model.add(Dropout(0.1))
# model.add(kr.layers.Conv2D(128,kernel_size=(7, 7),activation='relu'))
# model.add(Dropout(0.15))
# model.add(kr.layers.MaxPooling2D(pool_size=(7, 7),))
# model.add(Dropout(0.25))
# model.add(Flatten())
# model.add(kr.layers.Dense(units=10, activation='softmax'))

model.add(kr.layers.Conv2D(64,kernel_size=(7, 7),activation='relu',input_shape=(28,28,1)))
BatchNormalization(axis=-1)
model.add(kr.layers.Conv2D(64,kernel_size=(7, 7),activation='relu',input_shape=(28,28,1)))
BatchNormalization(axis=-1)
model.add(kr.layers.MaxPooling2D(pool_size=(2, 2),))
model.add(kr.layers.Conv2D(128,kernel_size=(5, 5),activation='relu'))
model.add(kr.layers.Conv2D(256,kernel_size=(3, 3),activation='relu'))
model.add(kr.layers.MaxPooling2D(pool_size=(2, 2),))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(kr.layers.Dense(units=10, activation='softmax'))

""" model.add(kr.layers.Conv2D(32, (3, 3), input_shape=(28,28,1)))
model.add(kr.layers.Activation('relu'))
BatchNormalization(axis=-1)
model.add(kr.layers.Conv2D(32, (3, 3)))
model.add(kr.layers.Activation('relu'))
model.add(kr.layers.MaxPooling2D(pool_size=(2,2)))
BatchNormalization(axis=-1)
model.add(kr.layers.Conv2D(64,(3, 3)))
model.add(kr.layers.Activation('relu'))
BatchNormalization(axis=-1)
model.add(kr.layers.Conv2D(64, (3, 3)))
model.add(kr.layers.Activation('relu'))
model.add(kr.layers.MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
BatchNormalization()
model.add(Dense(512))
model.add(kr.layers.Activation('relu'))
BatchNormalization()
model.add(Dropout(0.2))
model.add(Dense(10))
model.add(kr.layers.Activation('softmax')) """ 



model.compile(loss=kr.losses.categorical_crossentropy,optimizer='adadelta',metrics=['accuracy'])
model.summary()
#model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

#model.fit(x_train, x_test, epochs=10, batch_size=128)

epoch = 1000

#history_callback = model.fit(x_train, y_train, batch_size=128,epochs=epoch ,verbose=1,validation_data=(x_test, y_test))

gen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08, shear_range=0.3,
                         height_shift_range=0.08, zoom_range=0.08)

test_gen = ImageDataGenerator()
#https://stackoverflow.com/questions/51748514/does-imagedatagenerator-add-more-images-to-my-dataset
#https://www.tensorflow.org/tutorials/keras/overfit_and_underfit
train_generator = gen.flow(x_train, y_train, batch_size=64)
test_generator = test_gen.flow(x_test, y_test, batch_size=64)


cbk = CustomModelCheckpoint()

history_callback= model.fit_generator(train_generator, steps_per_epoch=60000//64, epochs=epoch, 
                    validation_data=test_generator, validation_steps=10000//64, callbacks=[cbk])
#history_callback= model.fit_generator(train_generator, steps_per_epoch=60000//64, epochs=epoch, 
                  #  validation_data=test_generator, validation_steps=10000//64, callbacks=[cbk])

score = model.evaluate(x_test, y_test, verbose=0)

# accuracy on test data
val_accuracy = np.array(history_callback.history['val_accuracy'])
# loss on test data
val_loss =  np.array(history_callback.history['val_loss'])

#on train data
accuracy =  np.array(history_callback.history['accuracy'])
loss =  np.array(history_callback.history['loss'])

np.savetxt("val_accurracy1",val_accuracy,delimiter=",")
np.savetxt("val_loss1",val_loss,delimiter=",")
np.savetxt("accuracy1",accuracy,delimiter=",")
np.savetxt("loss1",loss,delimiter=",")

x = np.arange(0.0, epoch, 1)

plt.grid(True)

p1 = [0,epoch]
p2 = [0.995,0.995]


plt.plot(x,val_accuracy,x,accuracy,p1,p2)
plt.savefig('300_last1.png')
plt.show()
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save("cnn7776532nor1000.h5")



           
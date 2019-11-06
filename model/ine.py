import gzip
import numpy as np
import keras as kr
import sklearn.preprocessing as pre
import matplotlib.pyplot as plt
from keras.models import load_model


# Start a neural network, building it by layers.
model = kr.models.Sequential()

# Add a hidden layer with 1000 neurons and an input layer with 784.
model.add(kr.layers.Dense(units=600, activation='linear', input_dim=784))
model.add(kr.layers.Dense(units=400, activation='relu'))
# Add a three neuron output layer.
model.add(kr.layers.Dense(units=10, activation='softmax'))

# Build the graph.
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

with gzip.open('../mnist/train-images-idx3-ubyte.gz', 'rb') as f:
    train_img = f.read()

with gzip.open('../mnist/train-labels-idx1-ubyte.gz', 'rb') as f:
    train_lbl = f.read()

train_img = ~np.array(list(train_img[16:])).reshape(60000, 28, 28).astype(np.uint8) / 255.0
train_lbl =  np.array(list(train_lbl[ 8:])).astype(np.uint8)

inputs = train_img.reshape(60000, 784)

encoder = pre.LabelBinarizer()
encoder.fit(train_lbl)
outputs = encoder.transform(train_lbl)

print(train_lbl[0], outputs[0])

model.fit(inputs, outputs, epochs=2, batch_size=100)

with gzip.open('../mnist//t10k-images-idx3-ubyte.gz', 'rb') as f:
    test_img = f.read()

with gzip.open('../mnist//t10k-labels-idx1-ubyte.gz', 'rb') as f:
    test_lbl = f.read()

test_img = ~np.array(list(test_img[16:])).reshape(10000, 784).astype(np.uint8) / 255.0
test_lbl =  np.array(list(test_lbl[ 8:])).astype(np.uint8)

(encoder.inverse_transform(model.predict(test_img)) == test_lbl).sum()

#loss_and_metrics = model.evaluate(test_img, test_lbl, batch_size=100)


result = model.predict(test_img[1:2])
print(test_img[1:2])
print(result)


plt.imshow(test_img[1].reshape(28, 28), cmap='gray')
plt.show()
print("done")
model.save("first.h5")


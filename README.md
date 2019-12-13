# Handwritten digit recognition


This software allows to convert handwritten digits into computer form. The software has been developed in two stages: first a model was trained using Keras with Tensorflow as backend. Then that model has been used for creating a web app that allow the user to draw digits for making a prediction with the model that was first trained.


The application has been developed as part of Emerging Technologies course in Galway-Mayo Institute of Technologies.


### Model
  
A convolutional neural network created with Keras Tensorflow backend have been trained using Mnist dataset. The training process is documented in the Jupyter notebook. We show how the model improves by adding different layers, changing activation function and using augmented data.

 [Model](https://nbviewer.jupyter.org/github/JoseIgnacioRetamalThomsen/Emerging-Technologies-Assessment-2019/blob/master/model/Model.ipynb)

### Web app

The client has been design using bootstrap and chartjs. Its allow the user to draw a number using the mouse or touchscreen device, that can be composed by several digits. A sequence of images of how the number was draw is used for separate it in digits for them make individual predictions. The sequence is sent to a Flask application which processes the images for then response back with the prediction.

[Flask Web App](https://github.com/JoseIgnacioRetamalThomsen/Emerging-Technologies-Assessment-2019/blob/master/webapp/app.py)
 

 ## How to run
 
You may need to setup python environment as explained before. Anaconda have been used for install all packages so is the easiest way, you can install al packages separate if you want.

* Clone this repository

```
git clone https://github.com/JoseIgnacioRetamalThomsen/Emerging-Technologies-Assessment-2019.git

```

* go into folder and run flask

```
cd Emerging-Technologies-Assessment-2019/webapp
env flask run --host=0.0.0.0 --port=5000
```

* Use if want to remotly acces the app:

```
flask run --host=0.0.0.0 --port=5000
```

* You can acces app usign a web browser by the address 

```
http://127.0.0.1:5000/
```

or

```
http://%SERVER-IP%:5000/
```

## Enviroment Setup

Setup envirment using conda
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/

I have use conda for envirmonet setup:

* First Update conda


```
conda update conda

```


* Create enviroment, will use highest version of python


```
conda create -n env  anaconda

```

* Install kenras and tensoflow gpu


```
conda install -n env -c conda-forge keras tensorflow-gpu

```


* Activate env, install flask and corse

```

env activate
pip install Flask
pip install -U flask-cors

```


* Set path for enviroment from [https://stackoverflow.com/questions/20081338/how-to-activate-an-anaconda-environment](https://stackoverflow.com/questions/20081338/how-to-activate-an-anaconda-environment)

```
set PATH=C:\Anaconda\envs\env\Scripts;C:\Anaconda\envs\env;%PATH%

```


* Install cors

```
conda install -n env 
```

* Keras

```
conda install -c conda-forge keras tensorflow-gpu

pip install -U flask-cors
```

## Technologies

[Keras](https://keras.io/),  Deep learning library for python.

[Tensorflow](https://www.tensorflow.org/) Back end for keras.

[Anaconda](https://www.anaconda.com/) Python package.

[Flask](https://www.palletsprojects.com/p/flask/), web app framework.

[JQuery](https://jquery.com/) Javascript libarary.

[Bootstrap](https://getbootstrap.com/), web develop toolkit.

[Python](https://www.python.org/), programing language.

[CharJS](https://www.chartjs.org/), charts with javascript.

[Jupyter Notebook](https://jupyter.org/), interactive development enviroment.

# References

[MNIST data set](http://yann.lecun.com/exdb/mnist/)

[Big Endian and Little Endian](https://chortle.ccsu.edu/AssemblyTutorial/Chapter-15/ass15_3.html)

[Using neural nets to recognize handwritten digits](http://neuralnetworksanddeeplearning.com/chap1.html)

[Neurons in keras](https://github.com/ianmcloughlin/jupyter-teaching-notebooks/blob/master/keras-neurons.ipynb)

[Activation Functions](https://www.analyticsvidhya.com/blog/2017/10/fundamentals-deep-learning-activation-functions-when-to-use-them/)

[Categorical crossentropy](https://peltarion.com/knowledge-center/documentation/modeling-view/build-an-ai-model/loss-functions/categorical-crossentropy)

[Introduction to Loss Functions](https://algorithmia.com/blog/introduction-to-loss-functions)

[Gradient Descent](https://www.kdnuggets.com/2017/04/simple-understand-gradient-descent-algorithm.html)

[Introduction to Optimizers](https://algorithmia.com/blog/introduction-to-optimizers)

[Relu](https://medium.com/@danqing/a-practical-guide-to-relu-b83ca804f1f7)

[Difference of Activation Functions in Neural Networks in general](https://datascience.stackexchange.com/questions/14349/difference-of-activation-functions-in-neural-networks-in-general)

[Dropout](https://machinelearningmastery.com/dropout-regularization-deep-learning-models-keras/)

[A Comprehensive Guide to Convolutional Neural Networks ](https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53)

[Introduction to Pooling Layer](https://www.geeksforgeeks.org/cnn-introduction-to-pooling-layer/)

[A Gentle Introduction to Pooling Layers for Convolutional Neural Networks](https://machinelearningmastery.com/pooling-layers-for-convolutional-neural-networks/)

[Batch Normalization](https://arxiv.org/pdf/1502.03167v2.pdf)

[Batch normalization in Neural Networks](https://towardsdatascience.com/batch-normalization-in-neural-networks-1ac91516821c)

[Data Augmentation | How to use Deep Learning when you have Limited Data](https://medium.com/nanonets/how-to-use-deep-learning-when-you-have-limited-data-part-2-data-augmentation-c26971dc8ced)

 [MNIST_keras_CNN-99.55%](https://github.com/yashk2810/MNIST-Keras/blob/master/Notebook/MNIST_keras_CNN-99.55%25.ipynb)

 [tensorflow guide](https://www.tensorflow.org/guide/keras/)









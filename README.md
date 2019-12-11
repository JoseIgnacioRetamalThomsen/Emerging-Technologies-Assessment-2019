# Handwritten digit recognition

This software allows to convert handwritting digis into computer form. 

Implementation:

- Create a neural network using keras tensoflow then train it using Mnist datase.
- Develop a web app using flask and bootstrap.

### Enviroment Setup

Setup envirment using conda
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/

I have use conda for envirmonet setup:

* First Update conda

'' 
conda update conda
''

* Create enviroment, will use highest version of python

''
conda create -n env  anaconda
''

* Install kenras and tensoflow gpu

''
conda install -n env -c conda-forge keras tensorflow-gpu
''

* Activate env for install flask and corse

Path must be set ex: set PATH=C:\Anaconda\envs\env\Scripts;C:\Anaconda\envs\env;%PATH%

https://stackoverflow.com/questions/20081338/how-to-activate-an-anaconda-environment

''
env activate
pip install Flask
pip install -U flask-cors
''

* Install cors

''
conda install -n env 


serve

pip install tensorflow-serving-api


issue  with ssl

solved with 

https://stackoverflow.com/questions/54394764/pip-is-configured-with-locations-that-require-tls-ssl-however-the-ssl-module-i?rq=1

## Keras

conda install -c conda-forge keras tensorflow-gpu

pip install -U flask-cors

### How tO run

flask run --host=0.0.0.0 --port=80
### Contact


for kenras 
https://towardsdatascience.com/deploying-keras-models-using-tensorflow-serving-and-flask-508ba00f1037

93% -> 32 5x5, 64 3x3 , max poling 2x2 , flaten _> 128 , 10

## Technologies

https://keras.io/  Deep learning library for python

https://www.tensorflow.org/ BAck end for keras

https://www.anaconda.com/ Python package

https://www.palletsprojects.com/p/flask/ Web app framework

https://jquery.com/ Javascript libarary

https://getbootstrap.com/ Web develop toolkit

https://www.python.org/ Programing language

https://www.chartjs.org/ Easy charts with javascript


https://jupyter.org/ Interactive development enviroment.

# References

http://yann.lecun.com/exdb/mnist/

https://chortle.ccsu.edu/AssemblyTutorial/Chapter-15/ass15_3.html

http://neuralnetworksanddeeplearning.com/chap1.html

https://github.com/ianmcloughlin/jupyter-teaching-notebooks/blob/master/keras-neurons.ipynb

https://www.analyticsvidhya.com/blog/2017/10/fundamentals-deep-learning-activation-functions-when-to-use-them/

https://peltarion.com/knowledge-center/documentation/modeling-view/build-an-ai-model/loss-functions/categorical-crossentropy

https://algorithmia.com/blog/introduction-to-loss-functions

https://www.kdnuggets.com/2017/04/simple-understand-gradient-descent-algorithm.html

https://https://algorithmia.com/blog/introduction-to-optimizers.com/blog/introduction-to-optimizers

https://medium.com/@danqing/a-practical-guide-to-relu-b83ca804f1f7

https://datascience.stackexchange.com/questions/14349/difference-of-activation-functions-in-neural-networks-in-general

https://machinelearningmastery.com/dropout-regularization-deep-learning-models-keras/

https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53

https://www.geeksforgeeks.org/cnn-introduction-to-pooling-layer/

https://machinelearningmastery.com/pooling-layers-for-convolutional-neural-networks/

https://arxiv.org/pdf/1502.03167v2.pdf

https://towardsdatascience.com/batch-normalization-in-neural-networks-1ac91516821c

https://medium.com/nanonets/how-to-use-deep-learning-when-you-have-limited-data-part-2-data-augmentation-c26971dc8ced

 https://github.com/yashk2810/MNIST-Keras/blob/master/Notebook/MNIST_keras_CNN-99.55%25.ipynb

 https://www.tensorflow.org/guide/keras/









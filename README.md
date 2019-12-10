# Emerging-Technologies-Assessment-2019
Emerging Technologies Assessment 2019



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
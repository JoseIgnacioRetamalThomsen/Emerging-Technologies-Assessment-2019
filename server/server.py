
#modified from : https://palletsprojects.com/p/flask/

from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

    ### setup
    #  py -3 -m venv venv

    # venv\Scripts\activate 
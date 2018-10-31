#coding: utf-8

from flask import Flask, render_template, request
from flask import request
import time
import json
import hashlib

marvel_api_public_key = '9399a05df30b09d3e38fb1af1713c0c5'
marvel_api_private_key = '4f7daf1eaaa9e4100c83ff1f453e3d1a0abdd2d5'




app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/hero', methods=['GET'])
def search():
    query = request.args.get('query')

    time.sleep(2)

    json = {
        "figuras":[{"figura": 'images/comics/comic1.jpg', "active": "active"},
                    {"figura": 'images/comics/comic2.jpg', "active": ""},
                    {"figura": 'images/comics/comic3.jpg', "active": ""},
                    {"figura": 'images/comics/comic4.jpg', "active": ""},
                    {"figura": 'images/comics/comic5.jpg', "active": ""}
                    ]
    }
    return render_template("index.html", json=json, query=query)


@app.route('/hero/<nome>', methods=['GET'])
def get_info_hero(nome):
    pass


@app.route('/teste', methods=['GET'])
def teste():
    strJ = '{"funcionou": 200}'

    return strJ



def get_timestamp_now():
    return time.time()

def get_hash(date):
    h = hashlib.md5()
    h.update(date)
    return h.hexdigest()


if __name__ == "__main__":
    app.run(debug=True, port=8080)
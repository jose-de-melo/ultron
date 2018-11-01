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
    return render_template("index.html", status=201)


@app.route('/hero', methods=['GET'])
def search():
    query = request.args.get('query')

    time.sleep(5)

    json = {
        "figuras":[{"figura": 'images/comics/comic1.jpg', "active": "active"},
                    {"figura": 'images/comics/comic2.jpg', "active": ""},
                    {"figura": 'images/comics/comic3.jpg', "active": ""},
                    {"figura": 'images/comics/comic4.jpg', "active": ""},
                    {"figura": 'images/comics/comic5.jpg', "active": ""}
                    ]}

    twetts = {"twetts":[{"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 4,
      "data" : "14/02/2017",
      "cardClass" : "card"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 4.2,
      "data" : "14/02/2017",
      "cardClass" : "card p-3"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 1.2,
      "data" : "14/02/2017",
      "cardClass" : "card"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 3.1,
      "data" : "14/02/2017",
      "cardClass" : "card p-3"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 4.5,
      "data" : "14/02/2017",
      "cardClass" : "card"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 2,
      "data" : "14/02/2017",
      "cardClass" : "card p-3"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 3,
      "data" : "14/02/2017",
      "cardClass" : "card"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 1,
      "data" : "14/02/2017",
      "cardClass" : "card p-3"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 3.2,
      "data" : "14/02/2017",
      "cardClass" : "card"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 4.2,
      "data" : "14/02/2017",
      "cardClass" : "card p-3"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 4.2,
      "data" : "14/02/2017",
      "cardClass" : "card"},

      {"username": "joseslv13",
      "nickname" : "Zé",
      "conteudo" : "Captain America is the best Marvel Hero",
      "url_foto_perfil" : "images/me.jpg",
      "nota" : 4.2,
      "data" : "14/02/2017",
      "cardClass" : "card p-3"}
      
      ]
      
      }

    status = 200

    if query == 'erro':
        status = 404


    
    return render_template("index.html", json=json, query=query, t = twetts, status=status)


@app.route('/hero/<nome>', methods=['GET'])
def get_info_hero(nome):
    pass


def get_timestamp_now():
    return time.time()

def get_hash(date):
    h = hashlib.md5()
    h.update(date)
    return h.hexdigest()


if __name__ == "__main__":
    app.run(debug=True, port=8080)
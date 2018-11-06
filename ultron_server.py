#coding: utf-8

import json
from ModuloTwitter import twitter_module as tm
from ModuloMarvel import marvel_module as mm

from flask import Flask, render_template, request

app = Flask(__name__)

''' Rota para renderizar a página inicial da aplicação'''
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", status=201)


'''Busca por tweets que possuam determinado termo usando módulo'''
def search_tweets(termo):
    tweety = tm.Tweety()
    result = tweety.search_term(termo)
    return tweety.filter(result)


''' Busca pelo nome do herói fornecido utilizando módulo'''
def search_hero(heroName):
    marvelpi = mm.MarvelAPI()
    return marvelpi.filter(marvelpi.request_hero(heroName))


'''End-point para recuperar informações sobre o heroi'''
@app.route('/hero', methods=['GET'])
def search():
    query = request.args.get('name')

    if query == "":
        return render_template("index.html", status=404)

    jsonResponse = json.loads(search_hero(query))

    if jsonResponse['status'] == 404:
        return render_template("index.html", status=404)

    twetts = search_tweets("'"+query+"'")

    return render_template("index.html", hero=jsonResponse, query=query, t = twetts, status=200)

'''__main__'''
if __name__ == "__main__":
    app.run(debug=True, port=8080)

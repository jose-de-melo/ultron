#coding: utf-8

import json
from ModuloTwitter import twitter_module as tm
from ModuloMarvel import marvel_module as mm

from flask import Flask, render_template, request

app = Flask(__name__)

cache_marvel = "cache/"

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

''' Retorna as informações do heroi em cache, se não existir ele é criado'''
def marvel_cache_service(heroName):
    try:
        file = open('{}{}.marc'.format(cache_marvel,heroName),'r')
        text = file.read()
        file.close()
        return json.loads(text)
    except Exception:
        heroInfo = search_hero(heroName)
        jsn = json.loads(heroInfo)
        if(jsn['status'] != 404):
            file = open('{}{}.marc'.format(cache_marvel,heroName),'w')
            file.write(heroInfo)
            file.close()
        return jsn

''' Retorna os tweets do heroi recebidos, se não receber nenhum tenta retornar o cache'''
def twitter_cache_service(term):
    try:
        twetts = search_tweets("'{}'".format(term))
        file = open('{}{}.twec'.format(cache_marvel,term),'w')
        file.write(twetts)
        file.close()
        return json.loads(twetts)
    except Exception:
        try:
            file = open('{}{}.twec'.format(cache_marvel,term),'r')
            twetts = file.read()
            file.close()
            return json.loads(twetts)
        except Exception:
            return []


'''End-point para recuperar informações sobre o heroi'''
@app.route('/hero', methods=['GET'])
def search():
    query = request.args.get('name')

    if(query == ""):
        return render_template("index.html", status=404)

    heroInfo = marvel_cache_service(query)

    if(heroInfo['status'] == 404):
        return render_template("index.html", status=404)

    twetts = twitter_cache_service("'{}'".format(query))

    return render_template("index.html", hero=heroInfo, query=query, t = {'twetts':twetts}, status=200)

'''__main__'''
if __name__ == "__main__":
    app.run(debug=True, port=8080)

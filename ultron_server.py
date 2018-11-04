#coding: utf-8

import json
from ModuloTwitter import twitter_module as tm
from ModuloMarvel import marvel_module as mm

from flask import Flask, render_template, request

app = Flask(__name__)

'''Adiciona o callback da requisição antes do dado '''
def insert_callback(data):
    try:
        return "{0}({1})".format(request.args['callback'],data)
    except:
        return "{0}({1})".format('not callback' ,data)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", status=201)

'''URL de ajuda'''
@app.route('/help')
def help():
    jso = json.dumps({
        ' /help':'Retorna um json com as url e seus respectivos retornos',
        'GET /twitter/_termo_':'Busca o _termo_ na api do twitter e retorna um json contendo:nome, nick, profile_img_url, text',
        'GET /marvel/_hero_':'Busca pelo _hero_ na api da marvel e retorna um json com as informações do heroi'
    })
    return insert_callback(jso) 

'''End-point para recuperar tweets que possuam determinado termo'''
@app.route('/twitter/<termo>')
def tweet(termo):
    return insert_callback(search_tweets(termo))

def search_tweets(termo):
    tweety = tm.Tweety()
    result = tweety.search_term(termo)
    return tweety.filter(result)

'''End-point para recuperar informações sobre o heroi'''
@app.route('/marvel/<hero>')
def marvel_hero(hero):
    marvelpi = mm.MarvelAPI()
    return insert_callback( marvelpi.filter(marvelpi.request_hero(hero)) )


def search_hero(heroName):
    marvelpi = mm.MarvelAPI()
    return marvelpi.filter(marvelpi.request_hero(heroName))


def filtrar_comics(comic):
    if 'image_not_available' in comic['url_capa']:
        return False
    else:
        return True

@app.route('/hero', methods=['GET'])
def search():
    query = request.args.get('name')

    jsonResponse = json.loads(search_hero(query))

    if jsonResponse['status'] == 404:
        return render_template("index.html", status=404)

    comics = []

    for comic in jsonResponse['comics']:
        if filtrar_comics(comic):
            comics.append(comic)
        else:
            continue

    jsonResponse['comics'] = comics
    jsonResponse['comics'][0]['active'] = "active"

    twetts = search_tweets("'"+query+"'")

    return render_template("index.html", hero=jsonResponse, query=query, t = twetts, status=200)

'''__main__'''
if __name__ == "__main__":
    app.run(debug=True, port=8080)
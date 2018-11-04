#coding: utf-8

import time, hashlib, requests, json

''' 
 Classe que armazena as chaves de acesso e possui métodos para realizar requisições
à api da Marvel
'''
class MarvelAPI:
    public_key = '9399a05df30b09d3e38fb1af1713c0c5'
    private_key = '4f7daf1eaaa9e4100c83ff1f453e3d1a0abdd2d5'

    private_public_key = private_key + public_key

    url = 'https://gateway.marvel.com/v1/public/characters?name='

    '''Retorna o hash md5 do dado'''
    def get_hash(self, date):
        h = hashlib.md5()
        h.update(date.encode('utf-8'))
        return h.hexdigest()

    '''Retorna uma str com os paremetros de authorização'''
    def get_authorization(self):
        ts = time.time()

        return '&ts=' + str(ts) + '&apikey=' + self.public_key + '&hash=' + self.get_hash(str(ts)+self.private_public_key)

    '''Realiza uma requisição à api para obter informações do heroi'''
    def request_hero(self, hero):
        req = self.url + hero + self.get_authorization()

        return requests.get(req).text

    def filter(self, json_str):
        jsonResponse = json.loads(json_str)

        if jsonResponse['data']['count'] == 0:
            return json.dumps({"status": 404})

        hero = json.loads(json_str)['data']['results'][0]
        hero_out = {}
        hero_out['status'] = 200
        hero_out['nome'] = hero['name']
        hero_out['descricao'] = hero['description']
        hero_out['img_url'] = "{}.{}".format(hero['thumbnail']['path'],hero['thumbnail']['extension'])
        comics = []

        url_comics = "{}?{}".format(hero['comics']['collectionURI'], self.get_authorization())

        response = requests.get(url_comics).text
        comicsList = json.loads(response)['data']['results']

        firstComic = True
        for comic in comicsList:
            url_image_comic = {}

            if firstComic == True:
                url_image_comic['active'] = "active"
                firstComic = False
            else:
                url_image_comic['active'] = ""

            url_image_comic['url_capa'] = "{}.{}".format(comic['thumbnail']['path'], comic['thumbnail']['extension'])
            comics.append(url_image_comic)

        hero_out['comics'] = comics

        return json.dumps(hero_out)
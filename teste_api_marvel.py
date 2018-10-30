#coding: utf-8

import time
import hashlib
import requests


marvel_api_public_key = '9399a05df30b09d3e38fb1af1713c0c5'
marvel_api_private_key = '4f7daf1eaaa9e4100c83ff1f453e3d1a0abdd2d5'

hero = 'Iron Man'
url_marvel = 'https://gateway.marvel.com/v1/public/characters?name='


def get_timestamp_now():
    return time.time()

def get_hash(date):
    h = hashlib.md5()
    h.update(date.encode('utf-8'))
    return h.hexdigest()


def main():
    
    url = url_marvel + hero + get_complemento_url()

    r = requests.get(url)
    arq = open('response.json', 'w')
    arq.write(r.text)
    arq.close()
    print(r.text)


def get_complemento_url():
    ts = get_timestamp_now()
    return '&ts=' + str(ts) + '&apikey=' + marvel_api_public_key + '&hash=' + get_hash(str(ts)+marvel_api_private_key+marvel_api_public_key)

if __name__ == '__main__':
    main()
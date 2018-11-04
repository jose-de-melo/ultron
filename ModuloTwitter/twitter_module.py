#coding: utf-8

from TwitterAPI import TwitterAPI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import json, re

''' 
 Classe que armazena as chaves de acesso e possui métodos para realizar requisições
à api Twitter utilizando a biblioteca TwitterAPi
'''
class Tweety:
    keys = {
        "consumer_key":"09Zmx27gyLRh50GsPxa8S2LtQ",
        "consumer_secret":"uO7M4aGHGCK9oqxygrcgbxByCXcCLJMSTK72RmKBN9iLOXP4D3",
        "token_key":"1054111933014663168-VNtkKKAwLfNbpCpGZ5qsvczSMvRGZS",
        "token_secret":"6bfhp4oKxJ3lyVpKXyxu0jd2WGM66rSUXuWTmpzSsQZsv"
    }

    api = TwitterAPI(keys['consumer_key'],keys['consumer_secret'],
                     keys['token_key'],keys['token_secret'])

    '''end_points'''
    endp = {"search":"search/tweets"}

    '''Realiza uma busca pelo termo e retorna um TwitterResponse'''
    def search_term(self,term):
        return self.api.request(self.endp['search'], {'q':term,
                                                     'lang':'en'
                                                        })
    
    '''
     Filtra o TwitterResponse e retorna um json contendo apenas:
        ['user']['name'] == ['username']
        ['user']['screen_name']  == ['nickname']
        ['user']['profile_image_url'] == ['url_foto_perfil']
        ['text'] == ['conteudo']
        ['created_at'] == ['data']

        VaderSentimentResult == ['nota']

        Tembém retira as mensagens que estão truncadas
    '''
    def filter(self,tw_response):
        jso = []
        analyst = Skywalker()
        for tw in tw_response:
            if(not tw['truncated']):
                twt = {}
                twt['username'] = tw['user']['name']
                twt['nickname'] = tw['user']['screen_name']
                twt['url_foto_perfil'] = tw['user']['profile_image_url']
                twt['data'] = self.parse_date(tw['created_at'])
                twt['conteudo'] = tw['text']
                clean = self.tweet_cleaner(twt['conteudo'])
                scores = analyst.verify_polarity( str(clean.encode('utf-8')) )
                twt['nota'] = analyst.scores_to_nota(scores)
                twt['cardClass'] = "card"
                jso.append(twt)

        return {"twetts":jso}

    '''
        Transforma a data retornata pelo twitter em uma data no formato dd/MM/yyyy
    '''
    def parse_date(self, date):
        pattern_in = "%a %b %d %H:%M:%S %z %Y"
        pattern_out = "%d/%m/%Y"
        time = datetime.strptime(date, pattern_in)
        return time.strftime(pattern_out)
    
    def tweet_cleaner(self, text):
        pat1 = "@[A-Za-z0-9]+"
        pat2 = "https?://[A-Za-z0-9./]+"
        combined_pat = '|'.join((pat1, pat2))
        stripped = re.sub(combined_pat, '', text)
        letters_only = re.sub("[^a-zA-Z]", " ", stripped)
        return letters_only


'''
    Classe para realizar a analise sentimental de um texto atraves da
    ferramenta VADER-Sentiment-Analysis
'''
class Skywalker:
    '''Inicia uma variavel analyser que será usada em outras funções'''
    def __init__(self):
        self.analyser = SentimentIntensityAnalyzer()

    '''Define a polaridade do text e retorna uma string json com as seguintes informações:
        'pos' -> Porcentagem de chance de ser positivo
        'neu' -> Porcentagem de chance de ser neutro
        'neg' -> Porcentagem de chance de ser negativo
        'compound' -> if >= 0.05: positivo
                      if > -0.05 && < 0.05: neutro
                      if <= -0.05: negativo
        
        Os valores 'pos','neg' e 'neu' quando somados possuem o valor 1
    '''
    def verify_polarity(self, text):
        return self.analyser.polarity_scores(text)

    '''
        Transforma os scores retornados pelo vader para uma nota de 0-5
    '''
    def scores_to_nota(self, scores):
        valor = 0
        nota = 5.00
        comp = scores['compound']
        if(comp >= 0.05):
            valor = scores['pos'] if scores['pos'] > scores['neu'] else scores['neu']*0.75
        elif(comp <= -0.05):
            valor = 1.00 - scores['neg']
        else:
            valor = scores['neu'] * 0.5
        
        return (valor * nota)
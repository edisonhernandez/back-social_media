from TwitterSearch import *
import json #Libreria para manejar archivos JSON
from TweetClss import TweetG  # La clase Producto
from pymongo import MongoClient
from datetime import date
from datetime import datetime

import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    iam_apikey='SFj5IyCH4aVXwUgyGV4vXqg5rMMzALhbLw_3in4RZZKz',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)



hola = "";
hola2 = "";
url2="";
url3="";
url4="";
#Día actual
day = date(2019,9,2)
#Conexión al Server de MongoDB Pasandole el host y el puerto
#mongoClient = MongoClient('localhost',27017)
#Conexión a la base de datos
#db = mongoClient.ppython

#Obtener la coleccion
#collection = db.tweets
def obtener_bd():
    host = "localhost"
    puerto = "27017"
    usuario = "admin"
    palabra_secreta = "admin"
    base_de_datos = "ppython"
    cliente = MongoClient("mongodb://{}:{}".format(host, puerto))
    return cliente[base_de_datos]

def insertar(tweet):
    base_de_datos = obtener_bd()
    tweets = base_de_datos.tweets
    return tweets.insert_one({
        "created_at": tweet.created_at,
        "name": tweet.name,
        "username": tweet.username,
        "text": tweet.text,
        "location": tweet.location,
        "coordinates":tweet.coordinates,
        "place": tweet.place,
        "retweet_count":tweet.retweet_count,
        "statuses_count":tweet.statuses_count,
        "followers_count":tweet.followers_count,
        "friends_count":tweet.friends_count,
        "url":tweet.url
        
        }).inserted_id
def clean_tweet(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def obtener():
    base_de_datos = obtener_bd()
    return base_de_datos.tweets.find()

def sn(rr):
    #Categorías de respuesta
    pagina = rr
    print(pagina)
    response = natural_language_understanding.analyze(
        url=pagina,
        features=Features(categories=CategoriesOptions(limit=3))).get_result()
    print(json.dumps(response, indent=2))

    #Respuesta de conceptos

    response2 = natural_language_understanding.analyze(
       url=pagina,
        features=Features(concepts=ConceptsOptions(limit=3))).get_result()

    print(json.dumps(response2, indent=2))

    #Emoción
   # response3 = natural_language_understanding.analyze(
   #        url=pagina,
   #        features=Features(emotion=EmotionOptions())).get_result()

   # print(json.dumps(response3, indent=2))

    #Sentimiento
    response4 = natural_language_understanding.analyze(
        url=pagina,
        features=Features(sentiment=SentimentOptions())).get_result()

    print(json.dumps(response4, indent=2))
try:
    #analysis = TextBlob("RT @lizpastorch: Quiero hacer una denuncia. Hace prácticamente 4 meses mientras me encontraba fuera del país, sufrí una estafa en mi cuenta…")
    #print(analysis.sentiment)
    #an2 = analysis.translate(to='en')
    #print(an2.sentiment)
        
    tso = TwitterSearchOrder()
    tso.set_keywords(['movistar'])
    tso.set_language('es')
    tso.set_since(day)
    tso.set_geocode(-0.177727, -78.465829,15,imperial_metric=True)
    
    #tso.set_positive_attitude_filter()
    ts = TwitterSearch(
            consumer_key = 'tt9hxmB4nXMPkGM2X2sZB2QZi',
            consumer_secret = 'qVnKRRWLoL6t4hiw1uVEOAHtI4CMbfLJJautW9EpCyAUbHJKwT',
            access_token = '999027968683978753-UrAz3OQBtu0Wl3HG9o6AheDqHjGQSKM',
            access_token_secret = 'tzzT8ZLItqlIds3ygvWEgIWagOe4EppnE6On8dmN2Z2K0'
        )


    for tweet in ts.search_tweets_iterable(tso):
        text = tweet['text'];
        created_at = tweet['created_at'];
        name = tweet['user']['name'];
        username = tweet['user']['screen_name'];
        location = tweet['user']['location'];
        coordinates = tweet['coordinates']
        place = tweet['place'];
        retweet_count = tweet['retweet_count']
        statuses_count = tweet['user']['statuses_count']
        followers_count = tweet['user']['followers_count']
        friends_count = tweet['user']['friends_count']

        with open('data.json', 'a') as file:
            json.dump(tweet, file, indent=4)

        if 'extended_entities' in tweet:
             print("entroQQQQQ")
             
             for ur in tweet['extended_entities']['media']:
                url2 = ur['expanded_url']
             tt = TweetG(created_at,name,username,text,location,coordinates,place,retweet_count,statuses_count,followers_count,friends_count,url2)
             id = insertar(tt)
             sn(url2)
           
        elif len(tweet['entities']['urls']) > 0:
            print("entro2QQQQQ")
            for ur2 in tweet['entities']['urls']:
                    
                txt = ur2['expanded_url']
                x = txt.split("/")
                print(x)
                if x[2] == 'twitter.com':
                    
                    url3 = ur2['expanded_url']
                    tt = TweetG(created_at,name,username,text,location,coordinates,place,retweet_count,statuses_count,followers_count,friends_count,url3)
                    id = insertar(tt)
                    sn(url3)
            
                
        elif 'retweeted_status' in tweet:
            print("entro3QQQQ")
            for ur3 in tweet['retweeted_status']['entities']['urls']:
                txt = ur3['expanded_url']
                x = txt.split("/")
                print(x)
                if x[2] == 'twitter.com':
                    
                    url4 = ur3['expanded_url']
                    tt = TweetG(created_at,name,username,text,location,coordinates,place,retweet_count,statuses_count,followers_count,friends_count,url4)
                    id = insertar(tt)
                    sn(url4)
           
            #print("El id del producto insertado es: ", id)
            

        
        
        #response = natural_language_understanding.analyze(
        #url=url2,
        #features=Features(categories=CategoriesOptions(limit=3))).get_result()

        #print(json.dumps(response, indent=2))
        #print(json.dumps(response, indent=2)) 
       # print (tweet.text)
        #u=tweet.text
       # u=u.encode('unicode-escape').decode('utf-8')
        #an2 = hola.translate(from_lang='en',to='en')
        #print(hola)
        
        
        #print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
    #print("COMIENZAAAAAAAAAAAAAAA")
    #for producto in obtener():
        #print("text: ", producto["text"])
except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)

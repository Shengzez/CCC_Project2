import os
import re
import string
import sys
import reverse_geocoder as rg
import random
import matplotlib.pyplot as plt
import nltk
import json
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import googlemaps as gmaps
gmaps_key = gmaps.Client(key="AIzaSyCbIGvQr9YZ35mPLYTth4c_r1ViLAGOhrU")
#nltk.download('vader_lexicon')

def preprocessing(tweet):
    r1 = r'https?:/\/\S+'
    ## remove @people
    r2 = r'@[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…？“”‘’！\\]+'
    ##remove tag
    r3 = r'#[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…？“”‘’！\\]+'

    tweet = tweet.encode('utf-8', 'replace').decode('utf-8')
    tweet = re.sub(r1, "", tweet)
    tweet = re.sub(r2, "", tweet)
    tweet = re.sub(r3, "", str(tweet).lower().strip())
    return tweet


def analysistwi(t):
    outtwitter = {}
    cleantwi = preprocessing(t['text'])
    outtwitter['id'] = t['id']
    outtwitter["user"] = t["user"]
    outtwitter['text'] = cleantwi
    outtwitter["date"] = t["date"]
    outtwitter["hashtags"] = t["hashtags"]
    outtwitter["geo"] = t["geo"]
    outtwitter["bounding_box"] = t["bounding_box"]
    # lonsum = 0
    # latsum = 0
    # for lon, lat in t["bounding_box"][0]:
    #     lonsum += lon
    #     latsum += lat
    # long = lonsum / len(t["bounding_box"][0])
    # lati = latsum / len(t["bounding_box"][0])
    long1, lati1 = t["bounding_box"][0][0]
    long2, lati2 = t["bounding_box"][0][2]
    long = random.uniform(long1,long2)
    lati = random.uniform(lati1, lati2)
    reverse_geocode_result = gmaps_key.reverse_geocode((lati, long))
    outtwitter["geo_info"] = reverse_geocode_result[0]
    long = round(long, 3)
    lati = round(lati, 3)
    outtwitter["estimated_coordinate"] = (long,lati)
    result = rg.search((round(lati,1), round(long, 1)))
    place_result = rg.search((lati, long))
    suburb = result[0]['name']
    place = place_result[0]['name']
    outtwitter["suburb"] = suburb
    outtwitter["place"] = place
    analy = TextBlob(cleantwi)
    score = SentimentIntensityAnalyzer().polarity_scores(cleantwi)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']

    if neg > pos:
        outtwitter["sentiment"] = ('negative')
    elif pos > neg:
        outtwitter["sentiment"] = ('positive')
    else:
        outtwitter["sentiment"] = ('neutural')
    return outtwitter
'''

with open("/Users/guozihao0226/Desktop/COMP90024-2019S1-Team7-TrackerHub-master/scraper/Streamer/streamlog.txt", "r", encoding = "utf-8") as he:
    hef = he.readline()
    a = json.loads(hef)
    print(analysistwi(a))
'''

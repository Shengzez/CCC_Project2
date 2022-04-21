import os
import re
import string
import sys

import matplotlib.pyplot as plt
import nltk
import json
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
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
    #outtwitter["suburb"] = ""
    analy = TextBlob(cleantwi)
    score = SentimentIntensityAnalyzer().polarity_scores(cleantwi)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    #print(cleantwi)

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
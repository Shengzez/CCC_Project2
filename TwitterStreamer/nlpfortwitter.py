twi =[{"id": "1516333453389688836", "user": "sister_ratched", "text": "@ElizabethKamel Ha, yes!", "date": "2022-04-19 08:30:42+0000", "hashtags": [], "geo": [], "bounding_box": [[[148.995922, -35.48026], [148.995922, -35.147699], [149.263643, -35.147699], [149.263643, -35.48026]]]},
{"id": "1516333544729063427", "user": "JBPooket", "text": "Apparently some pensioners are already on the Indue Card. Oh... Did you mean white people?", "date": "2022-04-19 08:31:03+0000", "hashtags": [], "geo": [], "bounding_box": [[[140.961682, -39.15919], [140.961682, -33.980426], [149.976679, -33.980426], [149.976679, -39.15919]]]},
{"id": "1516333584516149250", "user": "Brettg04", "text": "@AFL Can we please stop punishing professional athletes because of what some shit parents do at an U8's footy game  in Melton \ud83c\udffc\u200d\u2642\ufe0f", "date": "2022-04-19 08:31:13+0000", "hashtags": [], "geo": [], "bounding_box": [[[144.593742, -38.433859], [144.593742, -37.511274], [145.512529, -37.511274], [145.512529, -38.433859]]]}]

import re
from textblob import TextBlob
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import string


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


import re
from textblob import TextBlob
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import string


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
    outtwitter['text'] = cleantwi
    outtwitter["bounding_box"] = t["bounding_box"]
    outtwitter["suburb"] = ""
    analy = TextBlob(cleantwi)
    score = SentimentIntensityAnalyzer().polarity_scores(cleantwi)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    print(cleantwi)

    if neg > pos:
        outtwitter["sentiment"] = ('negative')
    elif pos > neg:
        outtwitter["sentiment"] = ('positive')
    else:
        outtwitter["sentiment"] = ('neutural')
    return outtwitter



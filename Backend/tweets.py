from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from config import remote_server, DB_URI
import requests
import numpy as np

class Tweets(Resource):
    def __init__(self):
        self.db = remote_server['processed_tweets']

    def get(self, keyword):
        mango = {'selector': {'text': {'$regex': "\\b" + keyword + "\\b"}},
          'fields': ['id', 'text', 'suburb'],
          'limit': 10}

        response = jsonify(list(self.db.find(mango)))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

class Overall(Resource):
    def get(self):
        r = requests.get(DB_URI + f"/mel_tweets/_design/mel_all/_view/overall?reduce=true&group_level=1")
        r = r.json()
        res = {}
        for row in r['rows']:
            res[row['key']] = row['value']
        response = jsonify(res)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

class SentimentCount(Resource):
    def get(self, keyword):
        res = {}
        r = requests.get(DB_URI + f"/processed_tweets/_design/sentiment/_view/{keyword}?reduce=true&group_level=2")
        r = r.json()
        count = []

        for row in r['rows']:
            ky = row['key']
            if ky[0] not in res.keys():
                res[ky[0]] = {'name': ky[0].capitalize(), 'positive': 0, 'negative':0, 'neutural':0}
            res[ky[0]][ky[1]] += row['value']
        
        res['OVERALL'] = {'positive': 0, 'negative':0, 'neutural':0}
        max_tweet = 0
        min_tweet = 10000000
        for key in res.keys():
            if key == 'OVERALL' or key == 'Notfound': continue
            res[key]['positive_rate'] = (res[key]['positive'] + 0.5 * res[key]['neutural'])/ (res[key]['positive'] + res[key]['negative'] + res[key]['neutural'])
            res[key]['total'] = res[key]['positive'] + res[key]['negative'] + res[key]['neutural']
            
            if res[key]['total'] > max_tweet: max_tweet = res[key]['total']
            if res[key]['total'] < min_tweet: min_tweet = res[key]['total']
            
            res['OVERALL']['positive'] += res[key]['positive'] 
            res['OVERALL']['negative'] += res[key]['negative'] 
            res['OVERALL']['neutural'] += res[key]['neutural']

            count.append(res[key]['total'])
        
        Q1 = np.quantile(count,0.25, axis=0)
        Q3 = np.quantile(count,0.75, axis=0)
        iqr = 3*(Q3-Q1)
        for key in res.keys():
            if key == 'OVERALL' or key == 'Notfound': continue
            res[key]['number_rate'] = min(1, (res[key]['total'] - min_tweet) / (iqr - min_tweet))
        
        res['OVERALL']['max_tweet_number'] = max_tweet
        res['OVERALL']['min_tweet_number'] = min_tweet
        res['OVERALL']['3iqr'] = iqr
        res['OVERALL']['mean_tweet'] =  sum(count) / len(count)

        overall_r = requests.get(DB_URI + f"/mel_tweets/_design/mel_all/_view/overall?reduce=true&group_level=1")
        overall_r = overall_r.json()
        overall_res = {}
        for row in overall_r['rows']:
            overall_res[row['key']] = row['value']
        
        res['ALLMELB'] = overall_res

        response = jsonify(res)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

class SentimentAndRai(Resource):
    def get(self, keyword, year):
        self.db = remote_server['aurin_rai']
        res = {}
        count = []
        for item in self.db.view('_all_docs', include_docs=True):
            doc = item.doc
            res[doc['suburb']] = {'name': doc['suburb'].capitalize(), 'positive': 0, 'negative':0, 'neutural':0}
            res[doc['suburb']]['rai'] = doc[str(year)]
            count.append(doc[str(year)])

        res['OVERALL'] = {'min': np.min(count), 'max': np.max(count), "mean": np.mean(count)}

        r = requests.get(DB_URI + f"/processed_tweets/_design/sentiment/_view/{keyword}?reduce=true&group_level=2")
        r = r.json()

        for row in r['rows']:
            ky = row['key']
            if ky[0] not in res.keys():
                continue
            res[ky[0]][ky[1]] += row['value']
        
        for key in res.keys():
            if key == 'Notfound' or key == 'OVERALL': continue
            if (res[key]['positive'] + res[key]['negative'] + res[key]['neutural']) != 0: 
                res[key]['positive_rate'] = (res[key]['positive'] + 0.5 * res[key]['neutural'])/ (res[key]['positive'] + res[key]['negative'] + res[key]['neutural'])
            else:
                res[key]['positive_rate'] = None

        # print(res)
        response = jsonify(res)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

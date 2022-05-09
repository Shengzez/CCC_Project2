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

        return jsonify(list(self.db.find(mango)))

class SentimentCount(Resource):
    def __init__(self):
        self.db = remote_server['processed_tweets']

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

        response = jsonify(res)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


    '''
    USERS = [
        {"name": "zhangsan"},
        {"name": "lisi"},
        {"name": "wangwu"},
        {"name": "zhaoliu"}
    ]

    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('name', type=str, location='json', required=True, help="名字不能为空") \
            .parse_args()

        if args['name'] not in USERS:
            USERS.append({"name": args['name']})

        return jsonify(USERS)

    def delete(self):
        USERS = []
        return jsonify(USERS)
    '''

from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from config import remote_server, DB_URI
import requests


class Tweets(Resource):
    def __init__(self):
        self.db = remote_server['processed_tweets']

    def get(self, keyword):
        mango = {'selector': {'text': {'$regex': "\\b" + keyword + "\\b"}},
          'fields': ['id', 'text', 'suburb'],
          'limit': 10}

        return jsonify(list(self.db.find(mango)))

class AllTweets(Resource):
    def __init__(self):
        self.db = remote_server['processed_tweets']

    def get(self):
        res = {}
        r = requests.get(DB_URI + "/processed_tweets/_design/sentiment/_view/overall?reduce=true&group_level=2")
        r = r.json()
        for row in r['rows']:
            ky = row['key']
            if ky[0] not in res.keys():
                res[ky[0]] = {'name': ky[0].capitalize(), 'positive': 0, 'negative':0, 'neutural':0}
            res[ky[0]][ky[1]] += row['value']
        for key in res.keys():
            res[key]['positive_rate'] = res[key]['positive'] / (res[key]['positive'] + res[key]['negative'] + res[key]['neutural'])
        
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

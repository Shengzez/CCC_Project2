from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from config import remote_server


class Tweets(Resource):
    def __init__(self):
        self.db = remote_server['tweets']

    def get(self, keyword):
        mango = {'selector': {'text': {'$regex': "\\b" + keyword + "\\b"}},
          'fields': ['id', 'text', 'suburb'],
          'limit': 10}

        return jsonify(list(self.db.find(mango)))

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

from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from tweets import AllTweets, Tweets

app = Flask(__name__)
api = Api(app)

api.add_resource(Tweets, '/tweets/<keyword>')
api.add_resource(AllTweets, '/all_tweets')
api.init_app(app)

app.run(host='0.0.0.0', port=5555, use_reloader=True)
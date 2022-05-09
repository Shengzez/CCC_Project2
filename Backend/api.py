from aurin import AurinRai, AurinSeat
from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from tweets import SentimentCount, Tweets

app = Flask(__name__)
api = Api(app)

api.add_resource(Tweets, '/tweets/<keyword>')
api.add_resource(SentimentCount, '/sentiment/<keyword>')
api.add_resource(AurinRai, '/aurin/rai/<year>')
api.add_resource(AurinSeat, '/aurin/seat')
api.init_app(app)

app.run(host='0.0.0.0', port=5555, use_reloader=True)
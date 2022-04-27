from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from tweets import Tweets

app = Flask(__name__)
api = Api(app)

api.add_resource(Tweets, '/tweets/<keyword>')
api.init_app(app)

app.run(host='localhost', port=5555, use_reloader=True)
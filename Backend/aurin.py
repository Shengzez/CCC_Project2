from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from config import remote_server, DB_URI
import requests
import numpy as np

class AurinRai(Resource):

    def get(self, year):
        self.db = remote_server['aurin_rai']
        res = {}
        count = []
        for item in self.db.view('_all_docs', include_docs=True):
            doc = item.doc
            res[doc['suburb']] = doc[str(year)]
            count.append(doc[str(year)])
        res['OVERALL'] = {'min': np.min(count), 'max': np.max(count), "mean": np.mean(count)}
        
        response = jsonify(res)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

class AurinSeat(Resource):

    def get(self):
        self.db = remote_server['aurin_seat']
        res = {}
        count = []
        for item in self.db.view('_all_docs', include_docs=True):
            doc = item.doc
            res[doc['suburb']] = doc['seat']
            count.append(doc['seat'])
        res['OVERALL'] = {'min': float(np.min(count)), 'max': float(np.max(count)), "mean": float(np.mean(count))}
           
        response = jsonify(res)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
from flask import Flask, request,jsonify
from flask_restful import Resource, Api, reqparse
from createEmbedding import createEmbedding, get_similar_doc
from retriv import get_documents, get_query, get_ground_truth
from bm25 import get_bm25_idf
from flask_cors import CORS
import json
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
api = Api(app)
CORS(app)
sched = BackgroundScheduler(daemon=True)
sched.add_job(createEmbedding,'interval',minutes=1440)
sched.start()
class Query(Resource):
    def get(self):
        return {'hello': 'world'}
    def post(self):
        query = request.json['query']
        if query == "":
            return jsonify(msg="no query found")
        cosin_similarty = get_similar_doc(str(query))
        bm25_ranking = get_bm25_idf(query)
        return jsonify(bm_25=bm25_ranking, vsm=cosin_similarty)

class Ping(Resource):
    def get(self):
        return jsonify(msg="server is alive", address=request.host)


api.add_resource(Query, '/query')
api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run(debug=True)

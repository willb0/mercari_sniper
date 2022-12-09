from tinydb import TinyDB
from flask import Flask,request,jsonify
from flask_apscheduler import APScheduler
from models import SearchRequest
import requests
import os

MERCARI_SEARCH_URL = os.environ['mercari_url']

db = TinyDB('db.json')

app = Flask(__name__)

scheduler = APScheduler()

@app.route('/')
def home():
    return "Hello world"

@app.route('/searches/',methods = ['GET','POST'])
def searches():
    if request.method == 'GET':
        return jsonify(db.all())
    else:
        search = request.json
        try:
            req = SearchRequest(**search)
            db.insert(search)
        except:
            print('Could not parse your search request')
        return jsonify(req.json())

def search_mercari() -> None:
    print('searching mercari')
    searches = db.all()
    for search in searches:
        req = SearchRequest(**search)
        requests.post(MERCARI_SEARCH_URL,data=req.json())
    return 

if __name__ == '__main__':
    scheduler.add_job(id = 'mercari searches', func = search_mercari, trigger = 'interval', seconds = 60)
    scheduler.start()
    app.run(port=80)






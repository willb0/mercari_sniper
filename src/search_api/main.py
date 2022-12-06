from fastapi import FastAPI
from models import SearchRequest,SearchResponse,SignupRequest
from utils import aggregate,put_in_redis
import os
import redis


app = FastAPI()
r = redis.Redis(
    host = os.environ['REDIS_HOST'],
    port = os.environ['REDIS_PORT'],
    password = os.environ['REDIS_PASSWORD']
)

@app.post('/search_mercari')
def search(request:SearchRequest) -> SearchResponse:
    url,items = aggregate(request)
    res = SearchResponse(url=url,request=request,items=items[:request.num_items])
    redis_res = put_in_redis(request,res,r)
    # have redis response, now alert people who are subscribed to the search
    if redis_res != None:
        print('redis res is not none')
        number_str = 'search||' + request.json(ensure_ascii=False)
        print(number_str)
        number_res = r.get(number_str)
        if number_res:
            numbers = number_res.decode('utf-8').split('|')
            print('new items, texting these numbers')
            for number in numbers:
                print(number)
    return res

@app.post('/alert_signup')
def alert_signup(request:SignupRequest):
    # put in redis
    search = request.search.json(ensure_ascii=False)
    number = str(request.phone_number)
    redis_str = 'search||' + search
    res = r.get(redis_str)
    if res is None:
        res =  number + '|'
    else:
        res = res.decode('utf-8') + number + '|'
    r.set(redis_str,res)
    print(r.keys())
    return 

@app.post('/check')
def check():
    ct = 0
    for key in r.scan_iter():
        ct += 1
        print(key,r.get(key))
        if ct > 10:
            break




'''
redis_res = r.get(request_data)
        if redis_res != None:
            old,new = json.loads(redis_res),json.loads(res.json())
            print(jd.diff(old,new))
        r.set(request_data,res.json())
        print(r.keys())

import json
import jsondiff as jd

r = redis.Redis(
    host = os.environ['REDIS_HOST'],
    port = os.environ['REDIS_PORT'],
    password = os.environ['REDIS_PASSWORD']
)

'''
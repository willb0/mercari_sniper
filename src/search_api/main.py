from fastapi import FastAPI
from models import SearchRequest,SearchResponse,MercariItem
from utils import aggregate,put_in_redis
import json
import os
import redis
import jsondiff as jd
from fastapi.encoders import jsonable_encoder


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
    print(redis_res)
    return res

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
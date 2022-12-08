from fastapi import FastAPI
from models import SearchRequest,SearchResponse,SignupRequest
from utils import aggregate,put_in_redis
import os
import redis
from twilio.rest import Client

MERCARI_IMG_URL = "https://static.mercdn.net/item/detail/orig/photos/{}_1.jpg"
MERCARI_ITEM_URL = "https://jp.mercari.com/item/{}"
TWILIO_NUMBER = '+18056692671'

t = Client(
    os.environ['account_sid'],
    os.environ['auth_token']
)


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
    if redis_res != []:
        print('redis res is not none',redis_res)
        items = [MERCARI_ITEM_URL.format(item.item_id) for item in redis_res]
        item_str = '\n'.join(items[:5])
        number_str = 'search||' + request.json(ensure_ascii=False)
        print(number_str)
        number_res = r.get(number_str)
        if number_res:
            numbers = number_res.decode('utf-8').split('|')
            print('new items, texting these numbers')
            for number in numbers:
                msg = t.messages.create(
                    to='+1' + number,
                    from_=TWILIO_NUMBER,
                    body = 'new items for your search\n' + item_str 
                )
                print(msg.sid)

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
    return {number:request.search}

@app.post('/check')
def check():
    ct = 0
    for key in r.scan_iter():
        ct += 1
        print(key,r.get(key))
        if ct > 10:
            break


import schedule
import time
import requests
import json

ex = json.load(open('example.json'))

def task():
    requests.post('http://localhost:80/search_mercari',json=ex)

schedule.every(1).minutes.do(task)

while True:
    schedule.run_pending()
    time.sleep(1)
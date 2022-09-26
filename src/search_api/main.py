from fastapi import FastAPI
from models import SearchRequest,SearchResponse
from utils import aggregate


app = FastAPI()

@app.post('/search_mercari')
def search(request:SearchRequest) -> SearchResponse:
    url,items = aggregate(request)
    return SearchResponse(url=url,request=request,items=items)
    

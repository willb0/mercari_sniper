from pydantic import BaseModel
from typing import List


class MercariItem(BaseModel):
    name: str
    src: str
    item_id: str
    price: str


class SearchRequest(BaseModel):
    keywords: str
    category: str
    brand: List[str]
    clothing_size: bool
    sizes: List[str]
    new_order: bool

class SearchResponse(BaseModel):
    request : SearchRequest
    items : List[MercariItem]
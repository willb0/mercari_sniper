from pydantic import BaseModel
from typing import List
from enum import Enum


class MercariItem(BaseModel):
    name: str
    src: str
    item_id: str
    price: str


class Brand(str,Enum):
    number_nine = '873'
    bape = '136'
    visvim = '273'

class SearchRequest(BaseModel):
    keywords: str
    category: str
    brand: List[str] = ['visvim']
    clothing_size: bool
    sizes: List[str]
    new_order: bool

    class Config:
        use_enum_values = True


class SearchResponse(BaseModel):
    url: str
    request: SearchRequest
    items: List[MercariItem]

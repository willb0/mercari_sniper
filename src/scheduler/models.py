from pydantic import BaseModel
from typing import List


class SearchRequest(BaseModel):
    keywords: str
    category: str
    brand: List[str] = ['visvim']
    clothing_size: bool
    sizes: List[str]
    new_order: bool
    num_items:int

    class Config:
        use_enum_values = True
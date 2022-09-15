from typing import List,Dict
categories = {
    'all' : 2,
    'tops' : 30,
    'jackets': 31,
    'pants': 32,
    'shoes': 33,
    'bag': 34,
    'suit': 35,
    'hats': 36,
    'rings': 37,
    'glasses': 38,
    'watches': 39,
    'socks/leggings': 40,
    'boxers': 41,
    'misc': 42
}

brands = {
    'number nine':873,
    'bape': 136
}

sizes_clothing = {
    'S':2,
    'M':3,
    'L':4,
    'XL':5
}

sizes_shoes = {
    '9.5':136,
    '10':137,
    '10.5':138,
    '11': 139,
    '11.5':140,
    '12':141,
    'biggg': 143
}

def gen_brands(brand:List[str]) -> str:
    return '%2C'.join(map(lambda x:str(brands.get(x)),brand))

def gen_sizes(sizes:List[str],sz: Dict[str,int]) -> str:
    return '%2C'.join(map(lambda x:str(sz.get(x)),sizes))

def build_url(keywords:str,category:str,brand:List[str],clothing_size:bool,sizes:List[str],new_order:bool) -> str:
    '''A function that generates a Mercari JP search url from parameters'''
    url = 'http://jp.mercari.com/search?'
    kwrds = f'keyword={"%20".join(keywords.split())}'
    order='&sort=created_time&order=desc'
    url += kwrds
    if new_order:
        url += order
    url += f'&category_id={categories[category]}'
    url += f'&brand_id={gen_brands(brand)}'
    url += f'&status=on_sale'
    if clothing_size:
        url += f'&size_id={gen_sizes(sizes,sizes_clothing)}'
    else:
        url += f'&size_id={gen_sizes(sizes,sizes_shoes)}'
    return url
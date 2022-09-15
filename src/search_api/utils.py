from typing import List,Dict
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from models import MercariItem,SearchRequest

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

def build_url(request:SearchRequest) -> str:
    '''A function that generates a Mercari JP search url from parameters'''
    keywords = request.keywords
    new_order = request.new_order
    category = request.category
    brand = request.brand
    sizes = request.sizes
    clothing_size = request.clothing_size
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

def get_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = webdriver.Firefox()
    return driver

def get_page_source(driver:webdriver.Firefox,url:str):
    driver.get(url)
    try:
        elem = WebDriverWait(driver,4).until(EC.presence_of_element_located((By.CLASS_NAME,'mer-item-thumbnail')))
    except TimeoutException:
        print('loading took 2 long')
    return driver.page_source

def extract_items(page_source:str) -> List[str]:
    soup = BeautifulSoup(page_source,'html.parser')
    items = soup.find_all('mer-item-thumbnail')
    return items

def get_item_info(items:List[str]) -> List[MercariItem]:
    return_items = []
    for item in items:
        attrs = item.attrs
        print(attrs)
        name = attrs['item-name']
        src = attrs['src']
        item_id = src.split('/')[-1].split('_')[0]
        price = attrs['price']
        item = MercariItem(name=name,src=src,item_id=item_id,price=price)
        return_items.append(item)
    return return_items

def aggregate(request:SearchRequest) -> List[MercariItem]:
    url = build_url(request)
    driver = get_driver()
    source = get_page_source(driver,url)
    items = extract_items(source)
    return get_item_info(items)

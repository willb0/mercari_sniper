import streamlit as st
import requests
import os
from models import MercariItem, SearchRequest, SearchResponse
import random

API_URL = "http://search_api:80/search_mercari"
MERCARI_IMG_URL = "https://static.mercdn.net/item/detail/orig/photos/{}_1.jpg"
MERCARI_ITEM_URL = "https://jp.mercari.com/item/{}"

st.title("mercari sniper")

with st.form("mercari_item"):
    st.header("search mercari")
    keywords = st.text_input("input search keywords")
    category = st.selectbox(
        "Pick a category",
        [
            "all",
            "tops",
            "jackets",
            "pants",
            "shoes",
            "bag",
            "suit",
            "hats",
            "rings",
            "glasses",
            "watches",
            "socks",
            "boxers",
            "misc",
        ],
    )
    brands = st.multiselect(
        "Pick a brand", ["bape", "visvim", "number nine"], default="visvim"
    )
    clothes_or_shoes = st.checkbox("Check for shoe sizing")
    if clothes_or_shoes:
        sizes = st.multiselect(
            "Pick shoe sizes",
            ["9.5" "10", "10.5", "11", "11.5", "12", "biggg"],
            default=["11", "11.5"],
        )
    else:
        sizes = st.multiselect(
            "Pick clothing size", ["S", "M", "L", "XL"], default=["L", "XL"]
        )
    sort_by_new = st.checkbox(
        'uncheck to sort by mercari "relevancy"', value=True)
    num_items = st.slider('num items', min_value=1, max_value=20, value=5)
    submit = st.form_submit_button("Search")
    if submit:
        request = SearchRequest(
            keywords=keywords,
            category=category,
            brand=brands,
            clothing_size=clothes_or_shoes,
            sizes=sizes,
            new_order=sort_by_new,
            num_items=num_items
        )
        res = requests.post(API_URL, data=request.json()).json()
        # print(res)
        res = SearchResponse(**res)
        request_data = request.json()
        
        items = res.items
        image_urls = [MERCARI_IMG_URL.format(item.item_id) for item in items]
        item_urls = [MERCARI_ITEM_URL.format(item.item_id) for item in items]
        markdown_str = '''
        <a href="{}">
            <img src="{}" width=300 />
        </a>
        '''
        k = 0
        for img,item in zip(image_urls,item_urls):
            st.markdown(markdown_str.format(item,img),unsafe_allow_html=True)
            k+= 1
            if k > num_items:
                break
        


# search_api

This is a fastAPI service that takes search parameters for mercari japan

to get it up and running (python 3.10):
```sh
python3 -m venv env && source env/bin/activate
pip install -r requirements.txt
uvicorn src.search_api.main:app --reload
```
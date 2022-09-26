# search_api

This is a fastAPI service that takes search parameters for mercari japan

docker:
```sh
docker build . -t search_api
docker run --rm -p 80:80 -it search-api
```

to get it up and running (python 3.10):
```sh
python3 -m venv env && source env/bin/activate
pip install -r requirements.txt
uvicorn src.search_api.main:app --reload
```

hit localhost:80/docs for Swagger UI
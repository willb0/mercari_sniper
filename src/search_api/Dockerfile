FROM arm64v8/python:3.10-slim-buster

WORKDIR /usr/src/api
RUN apt-get update && apt-get install gcc -y
COPY requirements.txt /usr/src/api/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./ /usr/src/api/

EXPOSE 80

CMD ["uvicorn","main:api","--host","0.0.0.0","--port","80"]


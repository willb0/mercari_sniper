FROM arm64v8/python:3.10-slim-buster

WORKDIR /usr/src/api
RUN apt-get update \
&& apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr gcc python3-dev           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl
COPY requirements.txt /usr/src/api/requirements.txt

RUN pip install wheel
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./ /usr/src/api/

EXPOSE 80

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","80"]


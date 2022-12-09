FROM arm64v8/python:3.8-slim


WORKDIR /usr/src/scheduler
RUN apt-get update && apt-get install gcc -y
COPY requirements.txt /usr/src/scheduler/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./ /usr/src/scheduler/


EXPOSE 82

CMD ["python","scheduler.py"]
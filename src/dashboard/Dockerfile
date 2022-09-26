FROM arm64v8/python:3.8-slim


WORKDIR /usr/src/dashboard
RUN apt-get update && apt-get install gcc -y
COPY requirements.txt /usr/src/dashboard/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./ /usr/src/dashboard/


EXPOSE 81

CMD ["streamlit", "run", "dash.py", "--server.port","81"]
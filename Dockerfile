# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

ENV PROXY_HOST="0.0.0.0"
ENV PROXY_PORT=9899
ENV CLIENT_HOST="redis-db"
ENV CLIENT_PORT=6379
ENV CACHE_CAPACITY=10
ENV CACHE_EXPIRY=10

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /core /app/core
COPY app.py /app/app.py

CMD [ "python3", "app.py" ]
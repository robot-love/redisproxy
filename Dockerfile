# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app
COPY /core /app/core

CMD [ "python3", "app.py", "--config", "config.yml" ]
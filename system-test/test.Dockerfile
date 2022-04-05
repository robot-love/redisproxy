# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

ENV PROXY_HOST="redis-proxy"
ENV PROXY_PORT=9899
ENV CLIENT_HOST="redis-db"
ENV CLIENT_PORT=6379

COPY system-test/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /system-test/test_system.py /app/test_system.py

CMD [ "python3", "-m", "pytest" ,"-v" ]
# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

ENV PROXY_HTTP_HOST="redis-proxy-http"
ENV PROXY_HTTP_PORT=8080
ENV PROXY_RESP_HOST="redis-proxy-resp"
ENV PROXY_RESP_PORT=6380
ENV CLIENT_HOST="redis-db"
ENV CLIENT_PORT=6379

COPY system-test/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /system-test/test_http_proxy_service.py /app/test_http_proxy_service.py
COPY /system-test/test_resp_proxy_service.py /app/test_resp_proxy_service.py

CMD [ "python3", "-m", "pytest" ]
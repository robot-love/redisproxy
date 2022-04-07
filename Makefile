help:
	@echo Here are some helpful commands: 
	@echo		build		- create proxy container network and build images
	@echo		up		- launch proxy service
	@echo		run		- build and launch proxy service, leave running (build + up)
	@echo		sys-test	- run system tests
	@echo		unit-test	- run unit tests
	@echo		down		- shut down proxy service

build:
	@echo -- Building proxy container network --
	@docker-compose build -q

up:
	@echo -- Starting proxy service --
	@docker-compose up -d

down:
	@echo -- Tearing down proxy service --
	@docker-compose down

run: build up

test:
	@echo -- Runnign system tests --
	@docker network create proxy-net
	@docker-compose -f docker-compose.sys-test.yml build -q
	@docker-compose -f docker-compose.sys-test.yml up -d
	@docker build -f test.Dockerfile --tag redis-proxy-test-suite . -q
	@docker run --network proxy-net --name proxy-test redis-proxy-test-suite
	@docker-compose down
	@docker rm proxy-test

unit-test:
	@echo -- Running unit tests --
	@docker exec redis-proxy-http python -m pytest -v --durations=0
	@docker exec redis-proxy-resp python -m pytest -v --durations=0
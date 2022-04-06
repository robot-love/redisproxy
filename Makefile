help:
	@echo Here are some helpful commands: 
	@echo		build		- create proxy container network and build images
	@echo		up		- launch proxy service
	@echo		run		- build and launch proxy service, leave running (build + up)
	@echo		system-test	- run system tests
	@echo		unit-test	- run unit tests
	@echo		teardown	- shut down proxy service

build:
	@docker network create proxy-net
	@docker-compose build

up:
	@docker-compose up -d

run: build up

sys-test:
	@echo Setting up system test
	@echo ----------------------
	@docker build -f system-test/test.Dockerfile --tag redis-proxy-test-suite .
	@docker run --network proxy-net --name proxy-test redis-proxy-test-suite
	@docker rm proxy-test

unit-test:
	@echo Setting up unit test
	@echo ----------------------
	@docker exec redis-proxy python -m pytest -v --durations=0

teardown:
	@echo Tearing down proxy service
	@docker stop redis-proxy-http redis-instance
	@docker rm redis-proxy-http redis-instance
	@docker network rm proxy-net

test: run sys-test teardown

# Add known key-values to redis
# docker exec -it redis-instance redis-cli

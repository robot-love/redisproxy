help:
	@echo Here are some helpful commands: 
	@echo   build 		- create proxy container network and build images
	@echo   up    		- launch proxy service
	@echo   run   		- build and launch proxy service
	@echo 	teardown 	- clean up proxy service from docker

build:
	@docker network create proxy-net
	@docker-compose build

up:
	@docker-compose up -d

run: build up

teardown:
	@echo Tearing down proxy service
	@docker stop redis-proxy redis-instance
	@docker rm redis-proxy redis-instance
	@docker network rm proxy-net

test-suite:
	@echo Setting up system test
	@echo ----------------------
	@docker build -f system-test/test.Dockerfile --tag redis-proxy-test-suite .
	@docker run --network proxy-net --name proxy-test redis-proxy-test-suite
	@docker rm proxy-test

test: run test-suite teardown

# Add known key-values to redis
# docker exec -it redis-instance redis-cli

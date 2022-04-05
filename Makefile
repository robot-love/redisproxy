help:
	@echo Here are some helpful commands: 
	@echo   build 		- create proxy container network and build images
	@echo   up    		- launch proxy service
	@echo   run   		- build and launch proxy service
	@echo 	teardown 	- clean up proxy service from docker

build:
	docker network create proxy-net
	docker-compose build

up:
	docker-compose up -d

teardown:
	docker stop redis-proxy redis-instance
	docker rm redis-proxy redis-instance
	docker network rm proxy-net

test-setup:
	@echo Setting up system test
	@echo ----------------------
	@docker run -d --network=proxy-net --name curl-proxy-test alpine/curl:latest tail -f /dev/null
	@echo  \
	
test1:
	@echo Testing key retrieval from proxy
	@echo --------------------------------
	@docker exec curl-proxy-test curl -s redis-proxy:9899/hello
	@echo

test-teardown:
	@echo Stopping curl container
	@echo -----------------------
	@docker stop curl-proxy-test
	@docker rm curl-proxy-test
	@echo  \

test-suite: test-setup test1 test-teardown

test: build up test-suite teardown

run: build up

# Add known key-values to redis
# docker exec -it redis-instance redis-cli
	

	
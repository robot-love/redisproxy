# Redis Proxy

This is an implementation of a Redis db proxy, that caches requests using a least-frequently-used eviction policy.


## Instructions

To run the service in production, simply run the following command: ```make run```. This will start the HTTP service on port 8080, and the RESP protocol service on port 6379. To modify these parameters, simply edit the docker-compose.yml file.

To run system tests in development, run the following command: ```make test```. This will start the HTTP service on port 8080, and the RESP protocol service on port 6380, with the backing instance available at port 6379.

To run unit tests, run the following command: ```make run``` followed by ```make unit-test```. 

Additional commands are available by running ```make help```.

## High Level Architecture


The diagram below shows the high level architecture of the service. The service is composed of three parts: the redis instance, an HTTP server, and an RESP protocol server. The HTTP server is exposed on the standard port 8080, and the RESP server is exposed on the standard Redis port 6379. The Redis instance itself is not exposed; the `GET` commands supported by the RESP proxy effectively mirror the Redis commands and replies.

![img.png](img/img_2.png)

The sequence diagram shows the workflow of possible calls to the proxy server. The GET command is rate-limited using a `asyncio.Semaphore` that is initialized to an environment variable declared in the `docker-compose.yml` file. 

![img.png](img/img_1.png)

## Code Structure

![img.png](img/img.png)

### The Proxy

The Proxy class is designed to be as simple and minimal as possible. The constructor takes a client object and cache object by composition. The client object only needs to support a `get()` method, and the cache must support `get()` and `add()` methods. 

### The LRU Cache

The LRU cache is implemented using Python's `collections.OrderedDict` data structure, which is effectively a hash-map plus a doubly-linked list. The algorithmic complexity of both adding elements to the cache, moving an element to the end (as most-recently-used), and eviction of the least-recently used of the cache is **O(1)**. Initially, cache eviction performed an eviction of all expired elements, however since the complexity of that operation is effectively **O(n)**, the implementation was removed.

### The HTTP and RESP Servers

The HTTP and RESP servers are set up in effectively the same way. Both servers require request handlers as callbacks, which are defined different for each type. The HTTP server has the additional feature of parsing the HTTP requests and sending it to the handler.

The HTTP server provides the key/value lookup at the `http://<host>/<key>` endpoint. The RESP server parses requests according a simplified RESP protocol (GET only) and either returns the value for the key, returns no value, or returns an error if the command cannot be parsed.

The structure of the HTTP and RESP servers are effectively the same, each with a callback function that handles requests. This request handler calls the proxy's `get(key)` method.

## Time Spent

- LRUCache: approximately 2 hours, plus an hour or two for debugging and unit testing
- Proxy: maybe 1 hour total.
- HTTP Server: probably around 1 full day, including system tests
- RESP Server: about 1 day, including testing with a Redis client and a raw TCP socket and additional system tests
- Makefile: probably a full day to get all the commands right. This took longer than I expected as I needed to become familiar with all the appropriate docker commands
- Docker containers: probably a full day to get all the containers running, had some trouble figuring out how to set up the application network

## Requirements Met and Not Met

All requirements are met, except for _parallel concurrent requests_. The reason this was not implemented is that Python is effectively a single-threaded language due to the infamous global interpreter lock (GIL). The `Cache` class could be made to be thread-safe by adding a lock around any write operations and their conditionals, however it would not actually improve cache performance.

The alternative to Python's `multithreading` library is to use `multiprocessing`, which increases complexity as it requires `shared_memory` since processes do not share memory space. This `shared_memory` can only include "pickleable" (read, serializable) objects, which is not the case for the `Cache` class. A possible solution to this would be to pass in the `OrderedDict` object to the `shared_memory` instantiation, and then pass that `shared_memory` object to the `Cache` class constructor when spawning the separate processes. This would make the code more complex, as now we have to manage the `OrderedDict` cache outside of the `Cache` class, making it difficult to maintain the required invariance. 

For true parallelism, the proxy can be written in a language that truly supports multithreaded operations, such as C++ or Java.

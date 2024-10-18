# Memcached Cluster with Python Client

This project sets up a Memcached cluster using Docker and Docker Compose, with a Python client that distributes keys across the cluster using pymemcache's HashClient.

## Setup and Run


1. In the root folder Build and start the Docker containers:
    ```
    open the dynamic-conf.sh and put how many memcached / flask apps you want
    run
    ./dynamic-conf.sh
    ```
2. In the root folder Build and start the Docker containers:
    ```
    docker-compose up --build
    ```

## Stopping the Containers

To stop the containers, run:
```
docker-compose down
```


## Blog Setup
1. you need a venv/
2. a .env
3. specify a valid OUTPUT_DIR

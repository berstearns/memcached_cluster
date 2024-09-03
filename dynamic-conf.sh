#!/bin/bash

# Configuration
NUM_MEMCACHED=5  # Number of Memcached instances
NUM_FLASK=10      # Number of Flask app instances
NGINX_CONF="./nginx-dynamic.conf"
DOCKER_COMPOSE="./docker-compose-dynamic.yml"

# Generate Nginx configuration
generate_nginx_conf() {
    MEMCACHED_SERVERS=""

    for ((i=1; i<=NUM_MEMCACHED; i++)); do
        if [ $i -eq 1 ]; then
            MEMCACHED_SERVERS="memcached$i:11211"
        else
            MEMCACHED_SERVERS="$MEMCACHED_SERVERS,memcached$i:11211"
        fi
    done

    cat <<EOF > $DOCKER_COMPOSE
version: '3'

services:
EOF

    # Memcached services
    for ((i=1; i<=NUM_MEMCACHED; i++)); do
        cat <<EOF >> $DOCKER_COMPOSE
  memcached$i:
    image: memcached:latest
    container_name: memcached$i
    ports:
      - "1121$i:11211"
EOF
    done

    # Flask app services
    for ((i=1; i<=NUM_FLASK; i++)); do
        cat <<EOF >> $DOCKER_COMPOSE
  python-client$i:
    build: ./src
    container_name: python-client$i
    depends_on:
EOF

        for ((j=1; j<=NUM_MEMCACHED; j++)); do
            cat <<EOF >> $DOCKER_COMPOSE
      - memcached$j
EOF
        done

        cat <<EOF >> $DOCKER_COMPOSE
    environment:
      - PYTHONUNBUFFERED=1
      - MEMCACHED_SERVERS=$MEMCACHED_SERVERS
    tty: true
EOF
    done

    # Nginx service
    cat <<EOF >> $DOCKER_COMPOSE
  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
    depends_on:
EOF

    for ((i=1; i<=NUM_FLASK; i++)); do
        cat <<EOF >> $DOCKER_COMPOSE
      - python-client$i
EOF
    done

    cat <<EOF >> $DOCKER_COMPOSE
    volumes:
      - ./nginx-dynamic.conf:/etc/nginx/nginx.conf:ro
EOF

    # Generate Nginx configuration file
    cat <<EOF > $NGINX_CONF 
events {}

http {
    upstream flask_app {
EOF

    for ((i=1; i<=NUM_FLASK; i++)); do
        cat <<EOF >> $NGINX_CONF
        server python-client$i;
EOF
    done

    cat <<EOF >> ./nginx-dynamic.conf
    }

    server {
        listen 80;

        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF
}

# Generate the configuration files
generate_nginx_conf

echo "Nginx configuration and Docker Compose file generated successfully."


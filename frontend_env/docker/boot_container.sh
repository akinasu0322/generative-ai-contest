#!/bin/bash

docker build -t app-image:1.0 -f ./docker/Dockerfile .
docker run -v .:/app -p 5678:5678 -it app-image:1.0 /bin/bash
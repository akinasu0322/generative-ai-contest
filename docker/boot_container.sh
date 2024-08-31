#!/bin/bash

docker build -t gen-ai-contest-image:1.0 -f ./docker/Dockerfile .
docker run -v .:/app -p 5000:5000 -it gen-ai-contest-image:1.0 /bin/bash
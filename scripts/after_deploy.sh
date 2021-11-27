#!/bin/bash

echo "Start Build"
echo "Stop image"
docker rm $(docker stop $(docker ps -a -q --filter ancestor=run_with_me --format="{{.ID}}"))

echo "Delete image"
docker rmi $(docker images | grep 'run_with_me')

echo "Build image dev"
docker-compose --env-file .env.dev up -d

echo "Done"

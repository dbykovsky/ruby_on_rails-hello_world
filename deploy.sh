#!/bin/sh

# to create a new image called test 
docker build . -t test1
#to start containers using compose file
echo "Environment deployment has started"
docker-compose up &
sleep 7
#run checks and tests 
python docker_manager.py

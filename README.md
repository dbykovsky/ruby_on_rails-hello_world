
Quick Hello World Rails App running in Docker
====================
-  You might need to have [Python 2.7.x](https://www.python.org/download/releases/2.7/)
-  You might need to have [Docker library](https://docker-py.readthedocs.io/en/stable/) installed
-  You may need [Docker](https://docs.docker.com/) installed on your machine

This project is amied to
----------------------------
- Boots 6 environments, each with an instance of the rails app and a "client" that can curl
- Tests that the rails process is up
- Tests that the client in each environment can successfully reach the rails app in the environment, and that the rails app "hello world"s
- Sets up the environments as 5 "nodes" and one "master", so that each node can talk back and forth with the master but no node can talk to any other node
- Tests the above configuration

To start the project
----------------------
- Pull this project on the machine where you want to run this
- Run Command: *./deploy.sh*
This will do the following:
 1. Dockerfile - will create a new image using Rails base image
 2. docker-compose.yaml - will compose containers with desired configuration
 3. docker_manager.py  - will run checks and tests

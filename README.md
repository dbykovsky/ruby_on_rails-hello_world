# Take home question
The goal of this question is for you to spin up a scalable testing environment. To do this, you're going to need
a bit of sysadmin knowledge and a bit of testing knowledge.

This app will "hello world" when hit at the "/" path.



# SUMMARY

## I used Docker container to boot 6 environments with and Python script to run tests and checks for the configuration


## Files modified/added
 1. Dockerfile - to create a new image
 2. docker-compose.yaml - to compose containers with desired configuration.
 3. docker_manager.py  - to run checks and tests
 4. deploy.sh - to create an image, start containers, start tests

## Video

I recorded a [video](https://www.youtube.com/watch?v=bJm0_WoyOZc&feature=youtu.be) with detailed explanation on how this project works.
#!/bin/bash
set -ex

# SET THE FOLLOWING VARIABLES
# docker hub username
USERNAME=unclcd
# image name

IMAGE=things_service
docker build -t $USERNAME/$IMAGE:latest .
#!/bin/bash

docker stop vyrobenounas.postgres
docker rm vyrobenounas.postgres
docker rmi vyrobenounas/postgres:10
rm -rf data/

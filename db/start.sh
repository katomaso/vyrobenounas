#!/bin/bash

if [[ -z `docker images | grep vyrobenounas/postgres` ]]
then
	echo "Vytvarim IMAGE vyrobenounas/postgres:10"
	docker build -t vyrobenounas/postgres:10 .
else
	echo "Nalezen IMAGE vyrobenounas/postgres:10"
fi

if [[ -z `docker ps -a | grep vyrobenounas.postgres` ]]
then
	echo "Vytvarim CONTAINER vyrobenounas.postgres z vyrobenounas/postgres:10"
	if [[ -d `pwd`/data ]]
	then
		echo "Chyba: `pwd`/data jiz existuje!"
		exit 1
	else
		echo "Data databaze budou v `pwd`/data"
	fi
	docker run -d \
	           --name vyrobenounas.postgres \
	           -e POSTGRES_PASSWORD=vyrobenounas \
	           -e PGDATA=/var/lib/postgresql/data/pgdata \
	           -p 5432:5432 \
	           -v `pwd`/data:/var/lib/postgresql/data/pgdata \
	           "vyrobenounas/postgres:10"
	sleep 2
fi

if [[ -z `docker ps | grep vyrobenounas.postgres` ]]
then
	echo "Startuji CONTAINER vyrobenounas.postgres"
	docker start vyrobenounas.postgres
	sleep 1
else
	echo "CONTAINER vyrobenounas.postgres bezi"
fi

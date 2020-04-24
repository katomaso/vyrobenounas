# https://hub.docker.com/_/postgres/
FROM postgres:10
MAINTAINER Tomas Peterka <tomas@peterka.me>

RUN localedef -i cs_CZ -c -f UTF-8 -A /usr/share/locale/locale.alias cs_CZ.UTF-8
ENV LANG cs_CZ.utf8

# Add dictionary files and init fulltext czech variation
COPY dictionaries/czech* /usr/share/postgresql/9.6/tsearch_data/
COPY init.sql /docker-entrypoint-initdb.d/

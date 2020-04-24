Multishop
#########

Aplikace sdílených obchodů pro projekt vyrobenounas.cz.

Spuštění
========

Nutnost: docker, python3, OSX nebo Linux.

**TLDR;**::

   $ docker image pull postgres:10
   $ docker run -d --name market.postgres postgres:10

   $ python3 -m venv venv
   $ . venv/bin/activate.sh
   $ pip install -r requirements.txt requirements.git.txt
   $ python manage.py migrate
   $ python manage.py load_test_data
   $ python manage.py runserver


Nejdříve je nutné spustit docker se services jako je databáze a cache ::

  $ ./start.sh

Tento příkaz stáhne obraz postgres z docker hubu, přidá do něj české slovníky z
``db/`` a pustí skript pro jejich instalaci. Díky tomu je možné využívat full
text search. Spuštěný image pak zapisuje svá data do ``db/data/``.
Smazání databáze je záležitost napsání ``$ ./remove.sh``, což je pohodlné hlavně
pro testování migrací.


Vytvoříme virtualenv a jedině python3 ::

   $ python3 -m venv venv
   $ . venv/bin/activate.sh

do kterého se nainstalují všechny závislosti naší aplikace ::

   $ pip install -r requirements.txt requirements.git.txt

Pak už jen připravit databázi ::

   $ python manage.py migrate

a nepovinně nahrát testovací data ::

   $ python manage.py load_test_data

Server se spustí příkazem ::

   $ python manage.py runserver

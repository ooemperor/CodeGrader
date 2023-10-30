# Installation 
This file will document the necessary steps to install and run this project. 

## Requirements
This Guide will show the necessary steps for installing and running the project on Debian 11 Servers with Python 3.9. 

It is assumed that you already have setup such a server and have access with a root user. 

## General Steps
```
apt-get install -y python-dev libpq-dev
apt-get install -y pip
```

# Frontend
## Python Packages
```
pip install -r requirements.txt
```
# Backend
## Python Packages
```
pip install -r requirements.txt
```

## PostgreSQL 15
Installing PostgreSQL Version 15 (according to [PostgreSQL Installation](https://www.postgresql.org/download/linux/debian/))
```
apt update && sudo apt upgrade -y
sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt-get update
apt-get install postgresql-15
```
By default the only host that can access the database is "localhost". If access to the database shall be established from a different host

Setting up the database (must be done with postgres user):
```
createuser --username=postgres --pwprompt codeGrader
createdb --username=postgres --owner=codeGrader codeGraderDB
psql --username=postgres --dbname=codeGraderDB --command='CREATE ROLE codeGrader'
psql --username=postgres --dbname=codeGraderDB --command='GRANT codegrader TO "codeGrader"'
psql --username=postgres --dbname=codeGraderDB --command='ALTER SCHEMA public OWNER TO codeGrader'
psql --username=postgres --dbname=codeGraderDB --command='GRANT SELECT ON pg_largeobject TO codeGrader'

```

## Execution Service
For the execution Service we do need some additional packages,so we can create containers and more. 
```
apt-get install lxc libvirt0 libpam-cgfs bridge-utils uidmap
```

The installation of the lxc packages can be verified with the <code>lxc-ls</code> command. If the installation was succesful there should not be any output at this point.
If there was some kind of error during the installation, an error message would be shown. 

## Evaluation Service
The Evaluation Service does not need any additional packages, than what is already specified in the requirements.txt of the backend package. 
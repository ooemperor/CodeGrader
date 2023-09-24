# Installtion 
This file will document the necessary steps to install and run this project. 

## Requirements
This Guide will show the necessary steps for installing and running the project on Debian 11 Servers with Python 3.9. 

It is assumed that you already have setup such a server and have access with a root user. 

## General Steps
```
apt-get install -y pip
```

## Frontend
### Python Packages
```
pip install -r requirements.txt
```
## Backend
### Python Packages
```
pip install -r requirements.txt
```

### PostgreSQL 15
Installing PostgreSQL Version 15 (according to [PostgreSQL Installation](https://www.postgresql.org/download/linux/debian/))
```
apt update && sudo apt upgrade -y
sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt-get update
apt-get install postgresql-15
```

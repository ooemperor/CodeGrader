# Installation 
This file will document the necessary steps to install and run this project. 

# General
Within this documentation you will find a Guide on how to manually deploy/install the codeGrader.
In case you prefer a automated way to deploy the codeGrader there are ansible playbooks avaible in the deployment folder. 
In a productive deployment you might need to change some variables in the playbooks (e.g. Database Password)

This Guide will show the necessary steps for installing and running the project on Debian 11 or Debian 12 Servers with Python 3.9 or higher.  

It is assumed that you already have setup such a server and have access with a root user. 

# Full Installation
Following from here you can find all the needed steps for a full installation on a single host. 

Corresponding Ansbile playbook: ```full_setup.yml```

Install all apt packages including postgres:
```
apt-get install -y libpython3-dev libpq-dev lxc libvirt0 libpam-cgfs bridge-utils uidmap pip git
```
Verify the installation of the lxc with the lxc-ls command. It should return no output and no error. 
After that we need to append some changes in order to run unpriviliged LXC Containers for the Execution Service
```
echo "root:100000:65536" >>/etc/subuid
echo "root:100000:65536" >>/etc/subgid
echo "lxc.idmap = u 0 100000 65536" >>/etc/lxc/default.conf
echo "lxc.idmap = g 0 100000 65536" >>/etc/lxc/default.conf
```
Then continue with
```
apt update && apt upgrade -y
sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt-get update
apt-get install postgresql-15 -y
```


```
sudo su - postgres
createuser --username=postgres --pwprompt codeGrader
createdb --username=postgres --owner=codeGrader codeGraderDB
psql --username=postgres --dbname=codeGraderDB --command='CREATE ROLE codeGrader'
psql --username=postgres --dbname=codeGraderDB --command='GRANT codegrader TO "codeGrader"'
psql --username=postgres --dbname=codeGraderDB --command='ALTER SCHEMA public OWNER TO codeGrader'
psql --username=postgres --dbname=codeGraderDB --command='GRANT SELECT ON pg_largeobject TO codeGrader'
exit

```
Then proceed with to clone and install the software itself. 

```
cd /opt
rm -r /opt/CodeGrader
git clone https://github.com/ooemperor/CodeGrader.git
cd CodeGrader
pip install -r ./codeGrader/frontend/requirements.txt
pip install -r ./codeGrader/backend/requirements.txt
cd /opt/CodeGrader
mv setup_full.py setup.py
pip install .
```

If you are running some Version of python higher than 3.9, it could be that there is an Error about Externally Managed python. 
You can resolve this by running: 
```
 rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED
```

Then create a new admin User and an api key with:
```
cgDeployDB
cgAddApiToken -d <Description>

cgAddAdmin -u <username> -fn <first_name> -ln <last_name> -e <email> -p <password>
```



After this part is done, please place the Config Files at "/etc/codeGrader" and adapt the values in it according to your installation (ApiToken, Database Credentials and IP Adresses).


When this is done you can then startup all the services with: 
```
nohup cgApiBackend &
nohup cgEvaluationService &
nohup cgExecutionService &
nohup cgUserFrontend &
nohup cgAdminFrontend &
```

## Services
If you want to run the 5 steps above as services under linux, please visit the services folder where you can finde the .service files. \
\
On debian you would need to copy these in the ```/etc/systemd/system``` \
After moving the files in this directory complete the startup with the following commands:
```
systemctl daemon-reload

systemd enable cgApiBackend.service
systemd enable cgEvaluationService.service
systemd enable cgExecutionService.service
systemd enable cgUserFrontend.service
systemd enable cgAdminFrontend.service

systemctl start cgApiBackend.service
systemctl start cgEvaluationService.service
systemctl start cgExecutionService.service
systemctl start cgUserFrontend.service
systemctl start cgAdminFrontend.service
```

# Redeployment
If you made any changes in the Code and would like to redeploy the Applications, you can use the corresponding playbooks. 

```redeploy_full.yml```         Reinstalls the frontend and backend and restarts it. 

```redeploy_backend.yml```      Reinstall only the backend. 

```redeploy_frontend.yml```     Reinstall only the frontend. 

# Partial Information on specific parts
## General Steps
```
apt-get install -y python-dev libpq-dev
apt-get install -y pip git
```

# Frontend
## Python Packages
```
pip install -r codeGrader/frontend/requirements.txt
```
# Backend
Running the backend API after Installtion of the package.
```
cgApiBackend
```
## Python Packages
```
pip install -r codeGrader/backend/requirements.txt
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

The installation of the lxc packages can be verified with the ```lxc-ls --fancy``` command. If the installation was succesful there should not be any output at this point.
If there was some kind of error during the installation, an error message would be shown. 

## Evaluation Service
The Evaluation Service does not need any additional packages, than what is already specified in the requirements.txt of the backend package. 

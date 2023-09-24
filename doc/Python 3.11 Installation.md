# Installation of Python 3.11 on Debian 11

Using the following statements Python 3.11 can be installed on Debian 11 Servers without losing the current 3.9 Installtion. 

Run as root user:
```
wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz \
tar xzf Python-3.11.3.tgz \
cd Python-3.11.3
apt update
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
./configure --enable-optimizations
make -j `nproc`
make altinstall
```

Afterwards the installation can be verified by using <code>python3.11 --version</code>


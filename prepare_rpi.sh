#!/bin/bash -e
sudo echo "instaling "
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
sudo echo 'deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen' | tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get install build-essential python-dev -y
sudo apt-get install python-PIL -y -y
sudo apt-get install gcc python-dev -y

sudo mkdir /home/temp
echo "############# Install redis"

cd /home/temp
sudo wget http://download.redis.io/redis-stable.tar.gz
sudo tar xvzf redis-stable.tar.gz
cd redis-stable
sudo make
sudo #apt-get update
sudo #apt-get install -y mongodb

echo "############# Git lib install process"

cd /home/temp
sudo git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
cd /home/temp
sudo git clone https://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install
sudo
sudo cd home/temp
echo "############ Pip install process"
sudo pip install stopit
sudo pip install pymongo
sudo pip install w1thermsensor
sudo pip install python-dateutil
sudo pip install redis
sudo pip install ctypes
sudo pip install configparser
sudo pip install psutil

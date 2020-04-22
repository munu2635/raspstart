#! /bin/bash

echo "file_setting"

sudo apt-get install git 
sudo apt-get install python-pip
pip install spidev

git clone https://github.com/munu2635/raspstart.git 

cd raspstart/mjpg-streamer/mjpg-streamer-experimental/

sudo apt-get install cmake
sudo apt-get install libjpeg-dev
sudo apt-get install python-smbus
sudo apt-get install python-dev

make CMAKE_BUILD_TYPE=Debug

cd 

sed -e "19s/.*/sudo sh home/pi/raspstart/mjpg.sh &" /etc/rc.local 
sed -e "20 i/sudo -H -u pi usr/bin/python home/pi/raspstart/sensingData/sensingMain.py &" /etc/rc.local

sudo reboot


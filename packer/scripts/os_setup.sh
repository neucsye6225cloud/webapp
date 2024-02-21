#!/bin/bash

sudo setenforce 0
sudo dnf update -y
sudo dnf -y install python3.9
# sudo ln -fs /usr/bin/python3.9 /usr/bin/python
sudo dnf -y groupinstall development
# sudo mkdir -p /opt/webapp
sudo python3.9 -m pip install --upgrade pip
sudo dnf -y install unzip

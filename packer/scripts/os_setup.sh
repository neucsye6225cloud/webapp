#!/bin/bash

sudo dnf update -y
sudo setenforce 0
sudo dnf -y install python3.9
sudo ln -fs /usr/bin/python3.9 /usr/bin/python
sudo dnf -y groupinstall development
sudo mkdir -p webapp

# sudo python -m pip3 install --upgrade pip

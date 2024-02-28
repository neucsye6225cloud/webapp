#!/bin/bash

sudo setenforce 0
sudo dnf update -y
sudo dnf -y install python3.9
sudo dnf -y groupinstall development
sudo python3.9 -m pip install --upgrade pip
sudo dnf -y install unzip

#!/bin/bash

sudo dnf -y install mysql-server
sudo systemctl start mysqld.service

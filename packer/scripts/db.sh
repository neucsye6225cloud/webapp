#!/bin/bash

sudo dnf -y install mysql-server
sudo systemctl start mysqld

sudo systemctl enable mysqld

mysqladmin -u root password 'root'
mysql -e "CREATE DATABASE IF NOT EXISTS cloud;" -uroot -proot

#!/bin/bash

# MySQL configuration
DB_USER="root"
DB_PASSWORD="root"
DB_NAME="cloud"

# Install MySQL server
sudo apt-get update
sudo apt-get install mysql-server

# Start MySQL service
sudo service mysql start

# Create database and user
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
mysql -u root -p -e "CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"
mysql -u root -p -e "FLUSH PRIVILEGES;"

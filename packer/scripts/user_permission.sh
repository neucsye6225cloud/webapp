#!/bin/bash

sudo useradd -M -s /usr/sbin/nologin csye6225
sudo chown -R csye6225:csye6225 ./webapp
sudo chmod -R 664 /etc/systemd/system/
sudo chown -R csye6225:csye6225 /usr/bin/

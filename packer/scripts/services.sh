#!/bin/bash

sudo mv /tmp/csye6225.service /etc/systemd/system/
echo "SELINUX=permissive" | sudo tee /etc/selinux/config
sudo systemctl daemon-reload 
sudo systemctl enable csye6225.service
sudo systemctl start csye6225.service

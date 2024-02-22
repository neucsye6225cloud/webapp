#!/bin/bash

sudo mv /tmp/csye6225.service /etc/systemd/system/
sudo systemctl daemon-reload
echo "SELINUX=permissive" | sudo tee /etc/selinux/config
sudo systemctl enable csye6225.service

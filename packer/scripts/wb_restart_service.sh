#!/bin/bash

sudo mv /tmp/web_service_restart.service /etc/systemd/system/
sudo chown -R csye6225:csye6225 /etc/systemd/system/web_service_restart.service
# echo "SELINUX=permissive" | sudo tee /etc/selinux/config
# sudo systemctl daemon-reload 
sudo systemctl enable web_service_restart.service
#sudo systemctl start web_service_restart.service

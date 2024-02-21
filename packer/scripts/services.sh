#!/bin/bash

sudo mv /tmp/csye6225.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable csye6225.service

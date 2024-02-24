#!/bin/bash

sudo mkdir -p ./webapp
cd /tmp/
unzip webapp.zip -d ./webapp/
cd ./webapp
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --user

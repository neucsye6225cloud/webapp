#!/bin/bash

cd /tmp/
unzip webapp.zip -d /opt/
cd /opt/webapp
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

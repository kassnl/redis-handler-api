#!/usr/bin/env bash

apt-get update
apt-get install python-pip
pip install virtualenv
virtualenv flask
pip install flask
pip install redis==2.6.2
pip install python-json-logger==0.0.3
pip install boto
pip install SQLAlchemy==0.7.8
pip install PyMySQL==0.5

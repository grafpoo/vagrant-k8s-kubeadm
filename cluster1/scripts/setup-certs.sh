 #! /bin/bash
 apt install -y python-pip
 pip install pexpect

mkdir -p /vagrant/certs
 python3 /vagrant/scripts/create-certs.py

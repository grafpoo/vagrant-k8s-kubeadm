 #! /bin/bash
 apt install -y python-pip
 pip install pexpect

 python3 /vagrant/scripts/create-certs.py

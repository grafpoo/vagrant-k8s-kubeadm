#! /bin/bash

echo You will need to enter a password three times - it is the password for the CA cert
echo Hit \<return\> and let\'s get going
read NOVAR

mkdir -p ca
cd ca
openssl genrsa -des3 -out k8sCA.key 2048 
openssl req -x509 -new -nodes -key k8sCA.key -sha256 -days 1825 -out k8sCA.pem<<EOF
US
maryland
baltimore
home
basement
k8scert
nobody@example.com
EOF
cd ..

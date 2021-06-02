#!/bin/sh

#if [ "$#" -ne 1 ]
#then
#  echo "Usage: Must supply a domain"
#  exit 1
#fi

set -x

DOMAIN=cluster1-harbor.local

mkdir -p /vagrant/certs
cd /vagrant/certs

openssl genrsa -out $DOMAIN.key 2048
openssl req -new -key $DOMAIN.key -out $DOMAIN.csr<<EOF
US
maryland
baltimore
home
basement
k8scert
nobody@example.com


EOF

cat > $DOMAIN.ext << EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = $DOMAIN
EOF

openssl x509 -req -in $DOMAIN.csr -CA /vagrant/ca/k8sCA.pem -CAkey /vagrant/ca/k8sCA.key -CAcreateserial \
-out $DOMAIN.crt -days 825 -sha256 -extfile $DOMAIN.ext

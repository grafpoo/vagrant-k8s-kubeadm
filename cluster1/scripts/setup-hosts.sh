#!/bin/bash
set -e
IFNAME=$1
ADDRESS="$(ip -4 addr show $IFNAME | grep "inet" | head -1 |awk '{print $2}' | cut -d/ -f1)"
sed -e "s/^.*${HOSTNAME}.*/${ADDRESS} ${HOSTNAME} ${HOSTNAME}.local/" -i /etc/hosts

# remove ubuntu-bionic entry
sed -e '/^.*ubuntu-bionic.*/d' -i /etc/hosts

cat > /etc/hosts<<EOF
127.0.0.1       localhost

192.168.11.8     cluster1-harbor cluster1-harbor.local
192.168.11.10    cluster1-master cluster1-master.local
192.168.11.11    cluster1-worker1 cluster1-worker1.local
192.168.11.12    cluster1-worker2 cluster1-worker2.local
192.168.11.13    cluster1-worker3 cluster1-worker3.local
192.168.11.14    cluster1-worker4 cluster1-worker4.local
192.168.11.15    cluster1-worker5 cluster1-worker5.local
192.168.11.16    cluster1-worker6 cluster1-worker6.local
192.168.11.17    cluster1-worker7 cluster1-worker7.local
192.168.11.18    cluster1-worker8 cluster1-worker8.local
EOF

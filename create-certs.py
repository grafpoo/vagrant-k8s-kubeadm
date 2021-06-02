#!/usr/bin/env python

'''This demonstrates an FTP "bookmark". This connects to an ftp site; does a
few ftp stuff; and then gives the user interactive control over the session. In
this case the "bookmark" is to a directory on the OpenBSD ftp server. It puts
you in the i386 packages directory. You can easily modify this for other sites.

PEXPECT LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2012, Noah Spurrier <noah@noah.org>
    PERMISSION TO USE, COPY, MODIFY, AND/OR DISTRIBUTE THIS SOFTWARE FOR ANY
    PURPOSE WITH OR WITHOUT FEE IS HEREBY GRANTED, PROVIDED THAT THE ABOVE
    COPYRIGHT NOTICE AND THIS PERMISSION NOTICE APPEAR IN ALL COPIES.
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

'''

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pexpect
import os
import sys
import subprocess

domain = sys.argv[1]

ca_keyfile_name = f"/vagrant/certs/{domain}CA.key"
ca_pemfile_name = f"/vagrant/certs/{domain}CA.pem"

ca_password = sys.argv[1] if len(sys.argv) > 1 else "password"

# create certificate authority

# generate CA keyfile

ca_key_command = f"openssl genrsa -des3 -out {ca_keyfile_name} 2048"
subprocess.call(["echo", ca_key_command])
child = pexpect.spawn(ca_key_command)

child.expect('.*', timeout=5)
child.sendline(ca_password)
child.expect('.*', timeout=5)
child.sendline(ca_password)

ca_pem_command = f"openssl req -x509 -new -nodes -key {ca_keyfile_name} -sha256 -days 1825 -out {ca_pemfile_name}"
subprocess.call(["echo", ca_pem_command])
child = pexpect.spawn(ca_pem_command)

child.expect('.*', timeout=5)
child.sendline(ca_password)
child.expect('Country.*\]:', timeout=5)
child.sendline('US')
child.expect('State.*\]:')
child.sendline('')
child.expect('Locality.*\]:')
child.sendline('')
child.expect('Organization.*\]:')
child.sendline('')
child.expect('Organizational.*\]:')
child.sendline('')
child.expect('Common.*\]:')
child.sendline(domain)
child.expect('Email.*\]:')
child.sendline('')

# now create certs for machines, signed by CA

for host in ["harbor", "gitlab"]:
    keyfile_name = f"/vagrant/certs/{domain}_{host}.key"
    csrfile_name = f"/vagrant/certs/{domain}_{host}.csr"
    extfile_name = f"/vagrant/certs/{domain}_{host}.ext"
    crtfile_name = f"/vagrant/certs/{domain}_{host}.crt"

    # generate key

    os.system(f"openssl genrsa -out {keyfile_name} 2048")
    #subprocess.call(["openssl", "genrsa", "-out", keyfile_name, "2048"])
    subprocess.call(["ls", keyfile_name])

    # generate csr

    csr_command = f"openssl req -new -key {keyfile_name} -out {csrfile_name}"
    subprocess.call(["echo", csr_command])
    child = pexpect.spawn(csr_command)

    child.expect('Country.*\]:', timeout=5)
    child.sendline('US')
    child.expect('State.*\]:')
    child.sendline('')
    child.expect('Locality.*\]:')
    child.sendline('')
    child.expect('Organization.*\]:')
    child.sendline('')
    child.expect('Organizational.*\]:')
    child.sendline('')
    child.expect('Common.*\]:')
    child.sendline(domain)
    child.expect('Email.*\]:')
    child.sendline('')
    child.expect('A challenge password.*\]:', timeout=5)
    child.sendline('')
    child.expect('An optional company name.*\]:', timeout=5)
    child.sendline('')

    # generate ext

    fext = open(extfile_name, "w")
    fext.write("authorityKeyIdentifier=keyid,issuer\n")
    fext.write("basicConstraints=CA:FALSE\n")
    fext.write("keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment\n")
    fext.write("subjectAltName = @alt_names\n")
    fext.write("[alt_names]\n")
    fext.write(f"DNS.1 = {domain}\n")
    fext.close()

    # generate certificate

    crt_command = f"openssl x509 -req -in {csrfile_name} -CA {ca_pemfile_name} -CAkey {ca_keyfile_name} -CAcreateserial -out {crtfile_name} -days 825 -sha256 -extfile {extfile_name}"
    subprocess.call(["echo", crt_command])
    child = pexpect.spawn(crt_command)

    child.expect('Enter.*', timeout=5)
    child.sendline(ca_password)


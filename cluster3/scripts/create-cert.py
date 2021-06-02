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
import sys
import subprocess

domain = sys.argv[0]
keyfile_name = f"{domain}.key"
csrfile_name = f"{domain}.csr"

subprocess.call(["openssl", "genrsa", "-out", keyfile_name, "2048"])


# Note that, for Python 3 compatibility reasons, we are using spawnu and
# importing unicode_literals (above). spawnu accepts Unicode input and
# unicode_literals makes all string literals in this script Unicode by default.
child = pexpect.spawnu(f"openssl req -new -key {keyfile_name} -out {csrfile_name}")

child.expect('Country .* []:')
child.sendline('US')
child.expect('State .* []:')
child.sendline('')
child.expect('Locality .* []:')
child.sendline('')
child.expect('Organization .* []:')
child.sendline('')
child.expect('Organizational .* []:')
child.sendline('')
child.expect('Common .* []:')
child.sendline(domain)
child.expect('Email .* []:')
child.sendline('')
if child.isalive():
    print('Child did not exit gracefully.')
    child.close()


'''
DOMAIN=$1

cd ~/certs

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

openssl x509 -req -in $DOMAIN.csr -CA ./ca/k8sCA.pem -CAkey ./ca/k8sCA.key -CAcreateserial \
-out $DOMAIN.crt -days 825 -sha256 -extfile $DOMAIN.ext

'''

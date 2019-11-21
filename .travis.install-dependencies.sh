#!/bin/bash

# Best practice for Travis CI is to use Python virtualenv instead of the system Python.
# Unfortunately, the virtualenv which Travis CI sets up has a broken bsddb module,
# doesn't have PyCrypto preinstalled, and doesn't play nice with dependencies from
# the Armory .deb distribution, so we just use the system Python instead.

set -e

# Download and install Armory v0.96.0 plus prerequisites
LATEST="https://github.com/goatpig/BitcoinArmory/releases/download/v0.96/armory_0.96-gcc5.4_amd64.deb"

curl -LfsS --retry 10 -o 'armory.deb' "$LATEST"

sudo apt-get -q update
sudo apt-get -yq install gdebi-core
sudo gdebi -nq armory.deb

# Download, compile, and install prerequisites for bitcoinj wallets

curl -fsS --retry 10 https://bootstrap.pypa.io/get-pip.py | sudo python
sudo /usr/local/bin/pip install -q protobuf scrypt pylibscrypt coincurve pysha3 green pycrypto

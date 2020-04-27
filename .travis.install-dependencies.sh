#!/bin/bash

set -e

# Download and install Armory v0.93.3 plus prerequisites
# (v0.94+ is unsupported on Ubuntu 12.04 w/o recompiling libstdc++6)

LATEST="https://github.com/goatpig/BitcoinArmory/releases/download/v0.93.3/armory_0.93.3_ubuntu-64bit.deb"

curl -LfsS --retry 10 -o 'armory.deb' "$LATEST"

sudo apt-get -q update
sudo apt-get -yq install gdebi-core
#sudo gdebi -nq armory.deb Don't install armory until fixed crash

# Download, compile, and install prerequisites for bitcoinj wallets
pip3 install -r requirements.txt
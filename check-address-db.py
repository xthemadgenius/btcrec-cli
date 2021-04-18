#!/usr/bin/env python

# check-address-db.py -- Bitcoin address database creator for seedrecover
# Copyright (C) 2021 Stephen Rothery
#
# This file is part of btcrecover.
#
# btcrecover is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#
# btcrecover is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

from btcrecover import addressset
from btcrecover import btcrseed
import sys,argparse, atexit
from os import path

__version__ =  "1.9.0-CryptoGuide"

if __name__ == "__main__":
    print("Starting CheckAddressDB", __version__)

    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfilename",   nargs="?", default="addresses.db", help="the name of the database file (default: addresses.db)")
    parser.add_argument("--checkaddresses", nargs="*", help="Check whether a single address is present in the addressDB")
    parser.add_argument("--checkaddresslist", metavar="PATH", help="Check whether all of the addresses in a list file are present in the addressDB")

    # Optional bash tab completion support
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args()

    if not path.exists(args.dbfilename):
        sys.exit("Address database file not found...")

    print("Loading address database ...")
    addressdb = addressset.AddressSet.fromfile(open(args.dbfilename, "rb"))
    print("Loaded", len(addressdb), "addresses from database ...")

    addresses = []
    comments = []

    if args.checkaddresses:
        for address in args.checkaddresses:
            addresses.append(address)
            comments.append("")

    if args.checkaddresslist:
        with open(args.checkaddresslist) as addressistfile:
            print("Loading: ", args.checkaddresslist)
            for line in addressistfile:
                if len(line) < 2: continue
                address, comment = line.split("#")
                addresses.append(address.strip())
                comments.append(comment.strip())

    checklist = zip(addresses, comments)

    for address, comment in checklist:
        # Just use wallet base and walletethereum for now
        try:
            hash160 = btcrseed.WalletBase._addresses_to_hash160s([address]).pop()
        except:
            hash160 = btcrseed.WalletEthereum._addresses_to_hash160s([address]).pop()

        if hash160 in addressdb:
            print(address, "Found!", comment)
        else:
            print(address, "Not Found!", comment)



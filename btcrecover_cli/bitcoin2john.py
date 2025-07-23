#!/usr/bin/env python3

"""
bitcoin2john.py - Bitcoin wallet to John the Ripper hash converter

This module extracts wallet encryption data and converts it to a format
suitable for password cracking tools like John the Ripper.

Based on the original bitcoin2john.py by Dhiru Kholia and others.
Modernized and integrated into btcrecover-cli.
"""

import sys
import os
import logging
import struct
import traceback
import hashlib
import binascii
from pathlib import Path

try:
    from bsddb3.db import *
except ImportError:
    try:
        from bsddb.db import *
    except ImportError:
        print("Error: bsddb3 or bsddb package is required", file=sys.stderr)
        sys.exit(1)


class SerializationError(Exception):
    """Thrown when there's a problem deserializing or serializing"""
    pass


class BCDataStream:
    """Bitcoin data stream parser"""
    
    def __init__(self):
        self.input = None
        self.read_cursor = 0

    def clear(self):
        self.input = None
        self.read_cursor = 0

    def write(self, bytes_data):
        if self.input is None:
            self.input = bytes_data
        else:
            self.input += bytes_data

    def read_bytes(self, length):
        try:
            result = self.input[self.read_cursor:self.read_cursor + length]
            self.read_cursor += length
            return result
        except (IndexError, TypeError):
            raise SerializationError("attempt to read past end of buffer")

    def read_string(self):
        try:
            length = self.read_compact_size()
        except IndexError:
            raise SerializationError("attempt to read past end of buffer")
        return self.read_bytes(length)

    def read_compact_size(self):
        if not self.input or self.read_cursor >= len(self.input):
            raise SerializationError("attempt to read past end of buffer")
            
        size = self.input[self.read_cursor]
        if isinstance(size, str):
            size = ord(size)
        self.read_cursor += 1
        
        if size == 253:
            size = self._read_num('<H')
        elif size == 254:
            size = self._read_num('<I')
        elif size == 255:
            size = self._read_num('<Q')
        return size

    def read_uint32(self):
        return self._read_num('<I')

    def _read_num(self, format_str):
        try:
            (i,) = struct.unpack_from(format_str, self.input, self.read_cursor)
            self.read_cursor += struct.calcsize(format_str)
            return i
        except struct.error:
            raise SerializationError("failed to read number")


def open_wallet(wallet_path):
    """Open a Bitcoin wallet.dat file"""
    if not os.path.exists(wallet_path):
        raise FileNotFoundError(f"Wallet file not found: {wallet_path}")
    
    db = DB()
    try:
        result = db.open(wallet_path, "main", DB_BTREE, DB_RDONLY | DB_THREAD)
        if result is not None:
            raise Exception("Failed to open wallet database")
        return db
    except DBError as e:
        raise Exception(f"Database error: {e}")


def parse_wallet_data(db):
    """Parse wallet data and extract encryption information"""
    wallet_data = {
        'mkey': {},
        'ckeys': [],
        'encrypted': False
    }
    
    kds = BCDataStream()
    vds = BCDataStream()
    
    try:
        for key, value in db.items():
            kds.clear()
            kds.write(key)
            vds.clear() 
            vds.write(value)
            
            try:
                record_type = kds.read_string()
                if isinstance(record_type, bytes):
                    record_type = record_type.decode('utf-8', errors='ignore')
                
                if record_type == "mkey":
                    # Master key record
                    nID = kds.read_uint32()
                    encrypted_key = vds.read_string()
                    salt = vds.read_string()
                    derivation_method = vds.read_uint32()
                    derivation_iterations = vds.read_uint32()
                    other_params = vds.read_string()
                    
                    wallet_data['mkey'] = {
                        'nID': nID,
                        'encrypted_key': encrypted_key,
                        'salt': salt,
                        'derivation_method': derivation_method,
                        'derivation_iterations': derivation_iterations,
                        'other_params': other_params
                    }
                    wallet_data['encrypted'] = True
                    
                elif record_type == "ckey":
                    # Encrypted private key
                    public_key = kds.read_bytes(kds.read_compact_size())
                    encrypted_private_key = vds.read_bytes(vds.read_compact_size())
                    
                    wallet_data['ckeys'].append({
                        'public_key': public_key,
                        'encrypted_private_key': encrypted_private_key
                    })
                    
            except (SerializationError, struct.error, UnicodeDecodeError) as e:
                # Skip corrupted records
                logging.debug(f"Skipping corrupted record: {e}")
                continue
                
    except Exception as e:
        logging.error(f"Error parsing wallet: {e}")
        raise
    
    return wallet_data


def generate_john_hash(wallet_path, wallet_data):
    """Generate John the Ripper compatible hash"""
    if not wallet_data['encrypted'] or not wallet_data['mkey']:
        return None
    
    mkey = wallet_data['mkey']
    
    # Find the first encrypted private key
    if not wallet_data['ckeys']:
        return None
    
    ckey = wallet_data['ckeys'][0]  # Use first encrypted key
    
    # Convert binary data to hex strings
    encrypted_key_hex = binascii.hexlify(mkey['encrypted_key']).decode('ascii')
    salt_hex = binascii.hexlify(mkey['salt']).decode('ascii')
    encrypted_private_key_hex = binascii.hexlify(ckey['encrypted_private_key']).decode('ascii')
    
    # Create John the Ripper hash format
    # Format: $bitcoin$length$encrypted_key$salt_length$salt$iterations$encrypted_private_key_length$encrypted_private_key$derivation_method
    john_hash = (
        f"$bitcoin${len(encrypted_key_hex)//2}${encrypted_key_hex}"
        f"${len(salt_hex)//2}${salt_hex}"
        f"${mkey['derivation_iterations']}"
        f"${len(encrypted_private_key_hex)//2}${encrypted_private_key_hex}"
        f"${mkey['derivation_method']}"
    )
    
    wallet_name = os.path.basename(wallet_path)
    return f"{wallet_name}:{john_hash}"


def bitcoin2john(wallet_path, output_file=None):
    """
    Convert Bitcoin wallet to John the Ripper format
    
    Args:
        wallet_path: Path to wallet.dat file
        output_file: Optional output file path
        
    Returns:
        John hash string or None if wallet is not encrypted
    """
    try:
        # Open and parse wallet
        db = open_wallet(wallet_path)
        wallet_data = parse_wallet_data(db)
        db.close()
        
        # Generate John hash
        john_hash = generate_john_hash(wallet_path, wallet_data)
        
        if john_hash is None:
            print("No encrypted keys found in wallet", file=sys.stderr)
            return None
        
        # Output hash
        if output_file:
            with open(output_file, 'w') as f:
                f.write(john_hash + '\n')
            print(f"Hash written to: {output_file}")
        else:
            print(john_hash)
        
        return john_hash
        
    except Exception as e:
        print(f"Error processing wallet: {e}", file=sys.stderr)
        return None


def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert Bitcoin wallet to John the Ripper hash format",
        epilog="This tool extracts encryption information from Bitcoin wallet.dat files "
               "and converts it to a format suitable for password cracking with John the Ripper."
    )
    
    parser.add_argument(
        "wallet",
        help="Path to wallet.dat file"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: print to stdout)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    # Convert wallet
    result = bitcoin2john(args.wallet, args.output)
    
    if result is None:
        sys.exit(1)
    
    print(f"Successfully processed wallet: {args.wallet}", file=sys.stderr)


if __name__ == "__main__":
    main()
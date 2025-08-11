#!/usr/bin/env python3

"""
pywallet.py - Python 3 compatible Bitcoin wallet management and recovery tool

This module provides PyWallet functionality integrated with btcrecover-cli,
including wallet dumping, key extraction, and recovery operations.

Based on the original pywallet by jackjack-jj, modernized for Python 3
and integrated into the btcrecover ecosystem.
"""

import sys
import os
import json
import logging
import binascii
import hashlib
import struct
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

try:
    from bsddb3.db import *
except ImportError:
    try:
        from bsddb.db import *
    except ImportError:
        print("Error: bsddb3 or bsddb package is required", file=sys.stderr)
        sys.exit(1)

# Import from our existing bitcoin2john module for compatibility
from .bitcoin2john import (
    BCDataStream, SerializationError, open_wallet, parse_wallet,
    hash_160, public_key_to_bc_address, b58encode, Hash
)


class PyWalletError(Exception):
    """Custom exception for PyWallet operations"""
    pass


class WalletDumper:
    """Main class for wallet dumping and key extraction operations"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
    
    def dump_wallet(self, wallet_path: str, passphrase: Optional[str] = None, 
                   include_balance: bool = False) -> Dict[str, Any]:
        """
        Dump wallet contents including keys, addresses, and transactions
        
        Args:
            wallet_path: Path to wallet.dat file
            passphrase: Optional passphrase for encrypted wallets
            include_balance: Whether to include balance information
            
        Returns:
            Dictionary containing wallet data
        """
        if not os.path.exists(wallet_path):
            raise PyWalletError(f"Wallet file not found: {wallet_path}")
        
        self.logger.info(f"Dumping wallet: {wallet_path}")
        
        wallet_data = {
            'keys': [],
            'addresses': [],
            'transactions': [],
            'settings': {},
            'metadata': {
                'wallet_file': wallet_path,
                'encrypted': False,
                'version': None
            }
        }
        
        try:
            # Use our existing wallet parsing functionality
            db = open_wallet(wallet_path)
            
            def item_callback(record_type: str, d: Dict[str, Any]):
                self._process_wallet_record(record_type, d, wallet_data, passphrase)
            
            parse_wallet(db, item_callback)
            db.close()
            
            # Post-process the wallet data
            self._post_process_wallet_data(wallet_data, include_balance)
            
            self.logger.info(f"Wallet dump completed: {len(wallet_data['keys'])} keys, "
                           f"{len(wallet_data['addresses'])} addresses, "
                           f"{len(wallet_data['transactions'])} transactions")
            
            return wallet_data
            
        except Exception as e:
            raise PyWalletError(f"Failed to dump wallet: {e}")
    
    def _process_wallet_record(self, record_type: str, d: Dict[str, Any], 
                              wallet_data: Dict[str, Any], passphrase: Optional[str]):
        """Process individual wallet records"""
        
        if record_type == "key":
            # Unencrypted private key
            try:
                addr = public_key_to_bc_address(d['public_key'])
                private_key_hex = binascii.hexlify(d['private_key']).decode()
                compressed = len(d['public_key']) == 33
                
                wallet_data['keys'].append({
                    'address': addr,
                    'private_key': private_key_hex,
                    'public_key': binascii.hexlify(d['public_key']).decode(),
                    'compressed': compressed,
                    'encrypted': False
                })
                
                wallet_data['addresses'].append({
                    'address': addr,
                    'type': 'key',
                    'compressed': compressed
                })
                
            except Exception as e:
                self.logger.warning(f"Failed to process key: {e}")
        
        elif record_type == "ckey":
            # Encrypted private key
            wallet_data['metadata']['encrypted'] = True
            
            try:
                addr = public_key_to_bc_address(d['public_key'])
                compressed = len(d['public_key']) == 33
                
                key_entry = {
                    'address': addr,
                    'private_key': 'ENCRYPTED',
                    'encrypted_private_key': binascii.hexlify(d['encrypted_private_key']).decode(),
                    'public_key': binascii.hexlify(d['public_key']).decode(),
                    'compressed': compressed,
                    'encrypted': True
                }
                
                # If passphrase provided, attempt decryption
                if passphrase:
                    try:
                        decrypted_key = self._decrypt_private_key(
                            d['encrypted_private_key'], passphrase, wallet_data
                        )
                        if decrypted_key:
                            key_entry['private_key'] = binascii.hexlify(decrypted_key).decode()
                            key_entry['decryption_status'] = 'success'
                        else:
                            key_entry['decryption_status'] = 'failed'
                    except Exception as e:
                        key_entry['decryption_status'] = f'error: {e}'
                        self.logger.warning(f"Failed to decrypt key for {addr}: {e}")
                
                wallet_data['keys'].append(key_entry)
                
                wallet_data['addresses'].append({
                    'address': addr,
                    'type': 'ckey',
                    'compressed': compressed,
                    'encrypted': True
                })
                
            except Exception as e:
                self.logger.warning(f"Failed to process encrypted key: {e}")
        
        elif record_type == "mkey":
            # Master key information
            wallet_data['metadata']['master_key'] = {
                'id': d.get('nID'),
                'salt': binascii.hexlify(d['salt']).decode() if 'salt' in d else None,
                'iterations': d.get('nDerivationIterations'),
                'method': d.get('nDerivationMethod')
            }
        
        elif record_type == "tx":
            # Transaction data
            wallet_data['transactions'].append({
                'txid': d.get('tx_id'),
                'inputs': d.get('txIn', []),
                'outputs': d.get('txOut', []),
                'version': d.get('version'),
                'lock_time': d.get('lockTime')
            })
        
        elif record_type == "version":
            wallet_data['metadata']['version'] = d.get('version')
        
        elif record_type == "setting":
            setting_name = d.get('setting')
            if isinstance(setting_name, bytes):
                setting_name = setting_name.decode('utf-8', errors='ignore')
            wallet_data['settings'][setting_name] = d.get('value')
    
    def _decrypt_private_key(self, encrypted_key: bytes, passphrase: str, 
                           wallet_data: Dict[str, Any]) -> Optional[bytes]:
        """Attempt to decrypt an encrypted private key"""
        # This is a placeholder - would need full implementation
        # for actual decryption based on wallet encryption parameters
        self.logger.debug("Private key decryption not fully implemented")
        return None
    
    def _post_process_wallet_data(self, wallet_data: Dict[str, Any], include_balance: bool):
        """Post-process wallet data after extraction"""
        # Sort addresses and keys
        wallet_data['addresses'].sort(key=lambda x: x['address'])
        wallet_data['keys'].sort(key=lambda x: x['address'])
        
        # Add balance information if requested
        if include_balance:
            self._add_balance_info(wallet_data)
        
        # Add statistics
        wallet_data['statistics'] = {
            'total_keys': len(wallet_data['keys']),
            'encrypted_keys': sum(1 for k in wallet_data['keys'] if k['encrypted']),
            'unencrypted_keys': sum(1 for k in wallet_data['keys'] if not k['encrypted']),
            'total_addresses': len(wallet_data['addresses']),
            'total_transactions': len(wallet_data['transactions'])
        }
    
    def _add_balance_info(self, wallet_data: Dict[str, Any]):
        """Add balance information to addresses (placeholder)"""
        # This would integrate with blockchain API services
        # For now, just mark as placeholder
        for addr in wallet_data['addresses']:
            addr['balance'] = 'N/A - API integration needed'
    
    def export_wallet_data(self, wallet_data: Dict[str, Any], output_path: str, 
                          format_type: str = 'json') -> None:
        """
        Export wallet data in various formats
        
        Args:
            wallet_data: Wallet data dictionary
            output_path: Output file path
            format_type: Export format ('json', 'csv', 'txt')
        """
        if format_type.lower() == 'json':
            self._export_json(wallet_data, output_path)
        elif format_type.lower() == 'csv':
            self._export_csv(wallet_data, output_path)
        elif format_type.lower() == 'txt':
            self._export_txt(wallet_data, output_path)
        else:
            raise PyWalletError(f"Unsupported export format: {format_type}")
    
    def _export_json(self, wallet_data: Dict[str, Any], output_path: str):
        """Export wallet data as JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(wallet_data, f, indent=2, ensure_ascii=False)
    
    def _export_csv(self, wallet_data: Dict[str, Any], output_path: str):
        """Export wallet keys as CSV"""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Address', 'Private Key', 'Compressed', 'Encrypted'])
            
            for key in wallet_data['keys']:
                writer.writerow([
                    key['address'],
                    key['private_key'],
                    key['compressed'],
                    key['encrypted']
                ])
    
    def _export_txt(self, wallet_data: Dict[str, Any], output_path: str):
        """Export wallet data as readable text"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Bitcoin Wallet Dump\n")
            f.write("=" * 50 + "\n\n")
            
            # Metadata
            f.write("Wallet Information:\n")
            f.write(f"  File: {wallet_data['metadata']['wallet_file']}\n")
            f.write(f"  Version: {wallet_data['metadata']['version']}\n")
            f.write(f"  Encrypted: {wallet_data['metadata']['encrypted']}\n")
            f.write("\n")
            
            # Statistics
            stats = wallet_data['statistics']
            f.write("Statistics:\n")
            f.write(f"  Total Keys: {stats['total_keys']}\n")
            f.write(f"  Encrypted Keys: {stats['encrypted_keys']}\n")
            f.write(f"  Unencrypted Keys: {stats['unencrypted_keys']}\n")
            f.write(f"  Total Addresses: {stats['total_addresses']}\n")
            f.write(f"  Total Transactions: {stats['total_transactions']}\n")
            f.write("\n")
            
            # Keys and addresses
            f.write("Private Keys:\n")
            f.write("-" * 30 + "\n")
            for key in wallet_data['keys']:
                f.write(f"Address: {key['address']}\n")
                f.write(f"Private Key: {key['private_key']}\n")
                f.write(f"Compressed: {key['compressed']}\n")
                f.write(f"Encrypted: {key['encrypted']}\n")
                f.write("\n")


def pywallet_dump_wallet(wallet_path: str, passphrase: Optional[str] = None,
                        output_file: Optional[str] = None, format_type: str = 'json',
                        include_balance: bool = False, verbose: bool = False) -> Dict[str, Any]:
    """
    Main function to dump wallet data (compatible with CLI interface)
    
    Args:
        wallet_path: Path to wallet.dat file
        passphrase: Optional passphrase for encrypted wallets
        output_file: Optional output file path
        format_type: Export format ('json', 'csv', 'txt')
        include_balance: Whether to include balance information
        verbose: Enable verbose logging
        
    Returns:
        Dictionary containing wallet data
    """
    try:
        dumper = WalletDumper(verbose=verbose)
        wallet_data = dumper.dump_wallet(wallet_path, passphrase, include_balance)
        
        if output_file:
            dumper.export_wallet_data(wallet_data, output_file, format_type)
            print(f"Wallet data exported to: {output_file}")
        
        return wallet_data
        
    except Exception as e:
        print(f"Error dumping wallet: {e}", file=sys.stderr)
        return {}


def main():
    """Command line interface for pywallet functionality"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PyWallet - Bitcoin wallet management and recovery tool",
        epilog="This tool provides wallet dumping, key extraction, and export capabilities "
               "for Bitcoin wallet.dat files with Python 3 compatibility."
    )
    
    parser.add_argument(
        "wallet",
        help="Path to wallet.dat file"
    )
    
    parser.add_argument(
        "--passphrase", "-p",
        help="Passphrase for encrypted wallets"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=['json', 'csv', 'txt'],
        default='json',
        help="Export format (default: json)"
    )
    
    parser.add_argument(
        "--include-balance", "-b",
        action="store_true",
        help="Include balance information (requires API)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Dump wallet
    wallet_data = pywallet_dump_wallet(
        args.wallet, 
        args.passphrase, 
        args.output, 
        args.format,
        args.include_balance, 
        args.verbose
    )
    
    if not args.output and wallet_data:
        # Print summary to stdout
        stats = wallet_data.get('statistics', {})
        print(f"Wallet dump completed:")
        print(f"  Total keys: {stats.get('total_keys', 0)}")
        print(f"  Encrypted keys: {stats.get('encrypted_keys', 0)}")
        print(f"  Unencrypted keys: {stats.get('unencrypted_keys', 0)}")
        print(f"  Addresses: {stats.get('total_addresses', 0)}")
        print(f"  Transactions: {stats.get('total_transactions', 0)}")


if __name__ == "__main__":
    main()
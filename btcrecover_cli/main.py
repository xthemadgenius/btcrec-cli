#!/usr/bin/env python3

import argparse
import sys
import os
import subprocess
from pathlib import Path

def get_script_path():
    """Get the path to the btcrecover scripts"""
    current_dir = Path(__file__).parent.parent
    return current_dir

def run_btcrecover(args):
    """Run the btcrecover.py script with provided arguments"""
    script_path = get_script_path() / "btcrecover.py"
    if not script_path.exists():
        print(f"Error: btcrecover.py not found at {script_path}", file=sys.stderr)
        return 1
    
    cmd = [sys.executable, str(script_path)] + args
    try:
        result = subprocess.run(cmd, cwd=get_script_path())
        return result.returncode
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error running btcrecover: {e}", file=sys.stderr)
        return 1

def run_seedrecover(args):
    """Run the seedrecover.py script with provided arguments"""
    script_path = get_script_path() / "seedrecover.py"
    if not script_path.exists():
        print(f"Error: seedrecover.py not found at {script_path}", file=sys.stderr)
        return 1
    
    cmd = [sys.executable, str(script_path)] + args
    try:
        result = subprocess.run(cmd, cwd=get_script_path())
        return result.returncode
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error running seedrecover: {e}", file=sys.stderr)
        return 1

def run_seedrecover_batch(args):
    """Run the seedrecover_batch.py script with provided arguments"""
    script_path = get_script_path() / "seedrecover_batch.py"
    if not script_path.exists():
        print(f"Error: seedrecover_batch.py not found at {script_path}", file=sys.stderr)
        return 1
    
    cmd = [sys.executable, str(script_path)] + args
    try:
        result = subprocess.run(cmd, cwd=get_script_path())
        return result.returncode
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error running seedrecover_batch: {e}", file=sys.stderr)
        return 1

def run_create_address_db(args):
    """Run the create-address-db.py script with provided arguments"""
    script_path = get_script_path() / "create-address-db.py"
    if not script_path.exists():
        print(f"Error: create-address-db.py not found at {script_path}", file=sys.stderr)
        return 1
    
    cmd = [sys.executable, str(script_path)] + args
    try:
        result = subprocess.run(cmd, cwd=get_script_path())
        return result.returncode
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error running create-address-db: {e}", file=sys.stderr)
        return 1

def run_check_address_db(args):
    """Run the check-address-db.py script with provided arguments"""
    script_path = get_script_path() / "check-address-db.py"
    if not script_path.exists():
        print(f"Error: check-address-db.py not found at {script_path}", file=sys.stderr)
        return 1
    
    cmd = [sys.executable, str(script_path)] + args
    try:
        result = subprocess.run(cmd, cwd=get_script_path())
        return result.returncode
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error running check-address-db: {e}", file=sys.stderr)
        return 1

def run_bitcoin2john(args):
    """Run the bitcoin2john functionality with provided arguments"""
    try:
        from .bitcoin2john import bitcoin2john
        
        if not args:
            print("Error: wallet file path required", file=sys.stderr)
            return 1
        
        wallet_path = args[0]
        output_file = None
        
        # Parse simple arguments
        if len(args) > 2 and args[1] in ['-o', '--output']:
            output_file = args[2]
        
        result = bitcoin2john(wallet_path, output_file)
        return 0 if result else 1
        
    except ImportError as e:
        print(f"Error: Failed to import bitcoin2john module: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error running bitcoin2john: {e}", file=sys.stderr)
        return 1

def run_pywallet(args):
    """Run the pywallet functionality with provided arguments"""
    try:
        from .pywallet import pywallet_dump_wallet
        
        if not args:
            print("Error: wallet file path required", file=sys.stderr)
            return 1
        
        # Parse arguments
        wallet_path = args[0]
        passphrase = None
        output_file = None
        format_type = 'json'
        include_balance = False
        verbose = False
        
        i = 1
        while i < len(args):
            arg = args[i]
            if arg in ['-p', '--passphrase'] and i + 1 < len(args):
                passphrase = args[i + 1]
                i += 2
            elif arg in ['-o', '--output'] and i + 1 < len(args):
                output_file = args[i + 1]
                i += 2
            elif arg in ['-f', '--format'] and i + 1 < len(args):
                format_type = args[i + 1]
                if format_type not in ['json', 'csv', 'txt']:
                    print(f"Error: Invalid format '{format_type}'. Use: json, csv, txt", file=sys.stderr)
                    return 1
                i += 2
            elif arg in ['-b', '--include-balance']:
                include_balance = True
                i += 1
            elif arg in ['-v', '--verbose']:
                verbose = True
                i += 1
            else:
                print(f"Error: Unknown argument '{arg}'", file=sys.stderr)
                return 1
        
        # Run pywallet
        wallet_data = pywallet_dump_wallet(
            wallet_path, passphrase, output_file, format_type, include_balance, verbose
        )
        
        return 0 if wallet_data else 1
        
    except ImportError as e:
        print(f"Error: Failed to import pywallet module: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error running pywallet: {e}", file=sys.stderr)
        return 1

def show_version():
    """Show version information"""
    from . import __version__
    print(f"BTCRecover CLI v{__version__}")

def main():
    """Main CLI entry point"""
    # Check if we should show help for subcommands
    if len(sys.argv) >= 3 and sys.argv[2] == "--help":
        command = sys.argv[1]
        if command == "password":
            return run_btcrecover(["--help"])
        elif command == "seed":
            return run_seedrecover(["--help"])
        elif command == "batch":
            return run_seedrecover_batch(["--help"])
        elif command == "create-db":
            return run_create_address_db(["--help"])
        elif command == "check-db":
            return run_check_address_db(["--help"])
        elif command == "bitcoin2john":
            print("bitcoin2john - Convert Bitcoin wallet to John the Ripper hash format")
            print()
            print("Usage:")
            print("  btcrecover bitcoin2john <wallet.dat> [-o output_file]")
            print()
            print("Arguments:")
            print("  wallet.dat     Path to Bitcoin wallet.dat file")
            print()
            print("Options:")
            print("  -o, --output   Output file (default: print to stdout)")
            print()
            print("This tool extracts encryption information from Bitcoin wallet.dat files")
            print("and converts it to a format suitable for password cracking with John the Ripper.")
            return 0
        elif command == "pywallet":
            print("pywallet - Bitcoin wallet analysis and key extraction tool")
            print()
            print("Usage:")
            print("  btcrecover pywallet <wallet.dat> [options]")
            print()
            print("Arguments:")
            print("  wallet.dat     Path to Bitcoin wallet.dat file")
            print()
            print("Options:")
            print("  -p, --passphrase PASS    Passphrase for encrypted wallets")
            print("  -o, --output FILE        Output file path")
            print("  -f, --format FORMAT      Export format: json, csv, txt (default: json)")
            print("  -b, --include-balance    Include balance information")
            print("  -v, --verbose           Enable verbose output")
            print()
            print("This tool provides comprehensive wallet analysis including:")
            print("• Extract private keys and addresses")
            print("• Analyze wallet structure and transactions")
            print("• Export data in multiple formats")
            print("• Handle encrypted and unencrypted wallets")
            return 0
    
    parser = argparse.ArgumentParser(
        prog="btcrecover",
        description="Bitcoin wallet password and seed recovery tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
BTCRecover CLI provides both direct script access and convenience commands:

Direct Script Access (matches documentation):
  btcrecover.py --wallet wallet.dat --passwordlist passwords.txt
  seedrecover.py --mnemonic "abandon abandon abandon..." --addr 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
  create-address-db.py --dbfilename addresses.db --addresses-file addresses.txt
  check-address-db.py --dbfilename addresses.db --checksum-file checksums.txt
  bitcoin2john.py wallet.dat

Convenience Commands:
  btcrecover password --wallet wallet.dat --passwordlist passwords.txt
  btcrecover seed --mnemonic "abandon abandon abandon..." --addr 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
  btcrecover create-db --dbfilename addresses.db --addresses-file addresses.txt
  btcrecover check-db --dbfilename addresses.db --checksum-file checksums.txt
  btcrecover bitcoin2john wallet.dat -o wallet.hash
  btcrecover pywallet wallet.dat -p password -o keys.json -f json

For detailed help on each command, use:
  btcrecover <command> --help
  btcrecover.py --help
  seedrecover.py --help

Documentation: https://btcrecover.readthedocs.io/
        """
    )
    
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version information"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )
    
    # Password recovery subcommand
    password_parser = subparsers.add_parser(
        "password",
        help="Recover wallet passwords",
        description="Recover passwords for various cryptocurrency wallets"
    )
    password_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to btcrecover.py"
    )
    
    # Seed recovery subcommand
    seed_parser = subparsers.add_parser(
        "seed",
        help="Recover mnemonic seeds",
        description="Recover mnemonic seed phrases for BIP39/BIP44 wallets"
    )
    seed_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to seedrecover.py"
    )
    
    # Batch seed recovery subcommand
    batch_parser = subparsers.add_parser(
        "batch",
        help="Batch seed recovery",
        description="Run multiple seed recovery operations in batch"
    )
    batch_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to seedrecover_batch.py"
    )
    
    # Create address database subcommand
    create_db_parser = subparsers.add_parser(
        "create-db",
        help="Create address database",
        description="Create an address database for wallet recovery"
    )
    create_db_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to create-address-db.py"
    )
    
    # Check address database subcommand
    check_db_parser = subparsers.add_parser(
        "check-db",
        help="Check address database",
        description="Check and verify an address database"
    )
    check_db_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to check-address-db.py"
    )
    
    # Bitcoin2john subcommand
    bitcoin2john_parser = subparsers.add_parser(
        "bitcoin2john",
        help="Convert wallet to John hash format",
        description="Convert Bitcoin wallet.dat to John the Ripper hash format"
    )
    bitcoin2john_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments: <wallet.dat> [-o output_file]"
    )
    
    # PyWallet subcommand
    pywallet_parser = subparsers.add_parser(
        "pywallet",
        help="Wallet analysis and key extraction",
        description="Comprehensive Bitcoin wallet analysis and key extraction"
    )
    pywallet_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments: <wallet.dat> [-p passphrase] [-o output] [-f format]"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle version
    if args.version:
        show_version()
        return 0
    
    # Handle no command
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate handler
    if args.command == "password":
        return run_btcrecover(args.args)
    elif args.command == "seed":
        return run_seedrecover(args.args)
    elif args.command == "batch":
        return run_seedrecover_batch(args.args)
    elif args.command == "create-db":
        return run_create_address_db(args.args)
    elif args.command == "check-db":
        return run_check_address_db(args.args)
    elif args.command == "bitcoin2john":
        return run_bitcoin2john(args.args)
    elif args.command == "pywallet":
        return run_pywallet(args.args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
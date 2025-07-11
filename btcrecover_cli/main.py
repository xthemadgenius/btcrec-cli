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

Convenience Commands:
  btcrecover password --wallet wallet.dat --passwordlist passwords.txt
  btcrecover seed --mnemonic "abandon abandon abandon..." --addr 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
  btcrecover create-db --dbfilename addresses.db --addresses-file addresses.txt
  btcrecover check-db --dbfilename addresses.db --checksum-file checksums.txt

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
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
extract_gui.py -- Terminal GUI for Bitcoin wallet extract scripts
Copyright (C) 2024 btcrecover contributors

This file is part of btcrecover.

btcrecover is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version
2 of the License, or (at your option) any later version.
"""

import os
import sys
import subprocess
import time
import glob
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'  # End formatting
    
    @staticmethod
    def green(text):
        return f"{Colors.GREEN}{text}{Colors.END}"
    
    @staticmethod
    def red(text):
        return f"{Colors.RED}{text}{Colors.END}"
    
    @staticmethod
    def yellow(text):
        return f"{Colors.YELLOW}{text}{Colors.END}"
    
    @staticmethod
    def blue(text):
        return f"{Colors.BLUE}{text}{Colors.END}"
    
    @staticmethod
    def bold(text):
        return f"{Colors.BOLD}{text}{Colors.END}"
    
    @staticmethod
    def success(text):
        return f"{Colors.GREEN}✓{Colors.END} {text}"
    
    @staticmethod
    def failure(text):
        return f"{Colors.RED}✗{Colors.END} {text}"
    
    @staticmethod
    def cyan(text):
        return f"{Colors.CYAN}{text}{Colors.END}"


class ExtractScriptRunner:
    def __init__(self, scripts_dir: str = None):
        self.scripts_dir = scripts_dir or os.path.join(os.path.dirname(__file__), "extract-scripts")
        self.scripts = self._discover_scripts()
        self.results = {}
        
    def _discover_scripts(self) -> List[Dict[str, str]]:
        """Discover all extract scripts in the scripts directory."""
        scripts = []
        pattern = os.path.join(self.scripts_dir, "extract-*.py")
        
        for script_path in glob.glob(pattern):
            script_name = os.path.basename(script_path)
            # Extract wallet type from filename
            wallet_type = script_name.replace("extract-", "").replace(".py", "")
            scripts.append({
                "name": script_name,
                "path": script_path,
                "type": wallet_type,
                "description": self._get_script_description(script_path)
            })
        
        return sorted(scripts, key=lambda x: x["name"])
    
    def _get_script_description(self, script_path: str) -> str:
        """Extract description from script docstring or comments."""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[:10]:  # Check first 10 lines
                    if "extractor" in line.lower() and line.strip().startswith("#"):
                        return line.strip("# \n")
            return "Bitcoin wallet data extractor"
        except Exception:
            return "Bitcoin wallet data extractor"
    
    def run_script(self, script: Dict[str, str], wallet_file: str) -> Tuple[bool, str, str]:
        """Run a single extract script against a wallet file."""
        try:
            cmd = [sys.executable, script["path"], wallet_file]
            
            # Run the script with timeout
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.scripts_dir
            )
            
            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            return success, stdout, stderr
            
        except subprocess.TimeoutExpired:
            return False, "", "Script execution timeout (30s)"
        except Exception as e:
            return False, "", f"Script execution error: {str(e)}"
    
    def run_all_scripts(self, wallet_file: str, callback=None) -> Dict[str, Dict]:
        """Run all extract scripts against a wallet file."""
        results = {}
        
        for i, script in enumerate(self.scripts):
            if callback:
                callback(i + 1, len(self.scripts), script["name"])
            
            success, stdout, stderr = self.run_script(script, wallet_file)
            
            results[script["name"]] = {
                "script": script,
                "success": success,
                "stdout": stdout,
                "stderr": stderr,
                "extracted_data": stdout if success and stdout else None
            }
        
        self.results = results
        return results


class TerminalGUI:
    def __init__(self):
        self.runner = ExtractScriptRunner()
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        print(Colors.blue("="*70))
        print(Colors.bold("  BTC Recovery - Extract Scripts Terminal GUI"))
        print(Colors.blue("="*70))
        print()
    
    def print_menu(self):
        """Print the main menu."""
        print("Options:")
        print("  1. List available extract scripts")
        print("  2. Run all scripts against a wallet file")
        print("  3. Run specific script against a wallet file")
        print("  4. Generate John the Ripper hash (bitcoin2john)")
        print("  5. PyWallet operations (comprehensive wallet management)")
        print("  6. Advanced PyWallet features (recovery, web interface, balance)")
        print("  7. View last results")
        print("  8. Exit")
        print()
    
    def list_scripts(self):
        """Display all available extract scripts."""
        self.clear_screen()
        self.print_header()
        
        print(f"Found {len(self.runner.scripts)} extract scripts:")
        print("-" * 70)
        
        for i, script in enumerate(self.runner.scripts, 1):
            print(f"{i:2d}. {script['name']}")
            print(f"     Type: {script['type']}")
            print(f"     Description: {script['description']}")
            print()
        
        input("\nPress Enter to continue...")
    
    def get_wallet_file(self) -> Optional[str]:
        """Get wallet file path from user."""
        while True:
            wallet_file = input("Enter wallet file path (or 'back' to return): ").strip()
            
            if wallet_file.lower() == 'back':
                return None
            
            if not wallet_file:
                print("Please enter a valid file path.")
                continue
            
            # Expand user path and make absolute
            wallet_file = os.path.expanduser(wallet_file)
            wallet_file = os.path.abspath(wallet_file)
            
            if not os.path.exists(wallet_file):
                print(f"Error: File '{wallet_file}' does not exist.")
                continue
            
            if not os.path.isfile(wallet_file):
                print(f"Error: '{wallet_file}' is not a file.")
                continue
            
            return wallet_file
    
    def progress_callback(self, current: int, total: int, script_name: str):
        """Progress callback for script execution."""
        percent = (current / total) * 100
        bar_length = 50
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        print(f'\r|{bar}| {percent:.1f}% - Running: {script_name}', end='', flush=True)
    
    def run_all_scripts(self):
        """Run all extract scripts against a wallet file."""
        self.clear_screen()
        self.print_header()
        
        print("Run All Extract Scripts")
        print("-" * 30)
        
        wallet_file = self.get_wallet_file()
        if not wallet_file:
            return
        
        print(f"\nRunning all {len(self.runner.scripts)} extract scripts against:")
        print(f"  {wallet_file}")
        print()
        
        # Run all scripts with progress display
        results = self.runner.run_all_scripts(wallet_file, self.progress_callback)
        
        print("\n\nResults:")
        print("=" * 70)
        
        successful_extractions = []
        failed_extractions = []
        
        for script_name, result in results.items():
            if result["success"] and result["extracted_data"]:
                successful_extractions.append((script_name, result))
                print(Colors.success(f"{script_name}: SUCCESS"))
            else:
                failed_extractions.append((script_name, result))
                print(Colors.failure(f"{script_name}: FAILED"))
        
        print(f"\nSummary: {Colors.green(str(len(successful_extractions)))} successful, {Colors.red(str(len(failed_extractions)))} failed")
        
        if successful_extractions:
            print(Colors.green("\nSuccessful extractions:"))
            for script_name, result in successful_extractions:
                print(f"\n{Colors.bold(script_name)}:")
                print(f"  Data: {Colors.green(result['extracted_data'][:80])}...")
        
        if failed_extractions:
            print(Colors.red("\nFailed extractions (with errors):"))
            for script_name, result in failed_extractions:
                if result["stderr"]:
                    print(f"\n{Colors.bold(script_name)}:")
                    print(f"  Error: {Colors.red(result['stderr'][:100])}...")
        
        input("\nPress Enter to continue...")
    
    def run_specific_script(self):
        """Run a specific extract script against a wallet file."""
        self.clear_screen()
        self.print_header()
        
        print("Run Specific Extract Script")
        print("-" * 30)
        
        # Show available scripts
        print("Available scripts:")
        for i, script in enumerate(self.runner.scripts, 1):
            print(f"{i:2d}. {script['name']} ({script['type']})")
        
        print()
        
        # Get script selection
        while True:
            try:
                choice = input("Enter script number (or 'back' to return): ").strip()
                if choice.lower() == 'back':
                    return
                
                choice = int(choice)
                if 1 <= choice <= len(self.runner.scripts):
                    selected_script = self.runner.scripts[choice - 1]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get wallet file
        wallet_file = self.get_wallet_file()
        if not wallet_file:
            return
        
        print(f"\nRunning {selected_script['name']} against:")
        print(f"  {wallet_file}")
        print()
        
        # Run the specific script
        success, stdout, stderr = self.runner.run_script(selected_script, wallet_file)
        
        print("Results:")
        print("=" * 50)
        
        if success and stdout:
            print(Colors.success(f"SUCCESS: {selected_script['name']}"))
            print(f"\nExtracted data:")
            print(Colors.green(stdout))
        else:
            print(Colors.failure(f"FAILED: {selected_script['name']}"))
            if stderr:
                print(f"\nError message:")
                print(Colors.red(stderr))
        
        input("\nPress Enter to continue...")
    
    def generate_john_hash(self):
        """Generate John the Ripper hash using bitcoin2john."""
        self.clear_screen()
        self.print_header()
        
        print("Generate John the Ripper Hash (bitcoin2john)")
        print("-" * 50)
        print()
        
        # Get wallet file
        wallet_file = self.get_wallet_file()
        if not wallet_file:
            return
        
        # Ask for output file
        output_file = input("Enter output file path (or press Enter for stdout): ").strip()
        if not output_file:
            output_file = None
        
        print(f"\nGenerating John hash from:")
        print(f"  {wallet_file}")
        if output_file:
            print(f"Output file: {output_file}")
        print()
        
        try:
            # Import bitcoin2john functionality
            print("Loading bitcoin2john module...")
            sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
            from btcrecover_cli.bitcoin2john import bitcoin2john
            print(Colors.success("Module loaded successfully"))
            
            # Validate wallet file
            print(f"Validating wallet file: {wallet_file}")
            if not os.path.exists(wallet_file):
                print(Colors.failure(f"Wallet file not found: {wallet_file}"))
                input("\nPress Enter to continue...")
                return
            
            file_size = os.path.getsize(wallet_file)
            print(f"Wallet file size: {file_size:,} bytes")
            
            if file_size == 0:
                print(Colors.failure("Wallet file is empty"))
                input("\nPress Enter to continue...")
                return
            
            # Generate the hash
            print("Processing wallet file...")
            print("- Opening wallet database")
            print("- Extracting encryption information")
            print("- Generating John the Ripper hash")
            
            result = bitcoin2john(wallet_file, output_file)
            
            if result:
                print()
                print("=" * 60)
                print(Colors.success("✓ John hash generated successfully!"))
                print("=" * 60)
                
                # Always show the hash preview for user experience
                print(f"\n{Colors.bold('Generated Hash Preview:')}")
                hash_preview = result if len(result) <= 120 else result[:120] + "..."
                print(f"{Colors.green(hash_preview)}")
                
                if output_file:
                    print(f"\n{Colors.bold('Output Details:')}")
                    print(f"  File: {Colors.cyan(output_file)}")
                    if os.path.exists(output_file):
                        output_size = os.path.getsize(output_file)
                        print(f"  Size: {output_size} bytes")
                        print(f"  Status: {Colors.green('File written successfully')}")
                        
                        # Show full hash from file for verification
                        try:
                            with open(output_file, 'r') as f:
                                file_hash = f.read().strip()
                            print(f"\n{Colors.bold('Full Hash (from file):')}")
                            print(f"{Colors.green(file_hash)}")
                        except Exception as e:
                            print(f"  Warning: Could not read hash from file: {e}")
                    else:
                        print(f"  Status: {Colors.red('Warning: Output file not found')}")
                else:
                    print(f"\n{Colors.bold('Complete Hash:')}")
                    print(f"{Colors.green(result)}")
                
                print(f"\n{Colors.bold('Next Steps:')}")
                print("1. Use the generated hash with John the Ripper:")
                print(f"   {Colors.cyan('john wallet.hash')}")
                print("2. Or with a wordlist:")
                print(f"   {Colors.cyan('john --wordlist=passwords.txt wallet.hash')}")
                print("3. Or with rules:")
                print(f"   {Colors.cyan('john --rules --wordlist=passwords.txt wallet.hash')}")
                
            else:
                print()
                print("=" * 60)
                print(Colors.failure("✗ Failed to generate John hash"))
                print("=" * 60)
                
                print(f"\n{Colors.bold('Diagnostic Information:')}")
                print(f"  Wallet file: {wallet_file}")
                print(f"  File exists: {Colors.green('Yes') if os.path.exists(wallet_file) else Colors.red('No')}")
                print(f"  File size: {file_size:,} bytes")
                print(f"  File readable: {Colors.green('Yes') if os.access(wallet_file, os.R_OK) else Colors.red('No')}")
                
                print(f"\n{Colors.bold('Possible Reasons:')}")
                print(f"  {Colors.yellow('•')} Wallet is not encrypted (no password protection)")
                print(f"  {Colors.yellow('•')} Wallet file is corrupted or invalid")
                print(f"  {Colors.yellow('•')} Not a Bitcoin Core wallet.dat file")
                print(f"  {Colors.yellow('•')} Wallet is currently in use by Bitcoin Core")
                print(f"  {Colors.yellow('•')} Database format not supported")
                
                print(f"\n{Colors.bold('Troubleshooting:')}")
                print("1. Ensure Bitcoin Core is closed")
                print("2. Verify this is an encrypted wallet.dat file")
                print("3. Try making a backup copy of the wallet")
                print("4. Check file permissions")
                
        except ImportError as e:
            print()
            print("=" * 60)
            print(Colors.failure("✗ Module Import Error"))
            print("=" * 60)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  {Colors.red(str(e))}")
            print(f"\n{Colors.bold('Possible Solutions:')}")
            print("1. Ensure btcrecover_cli module is properly installed")
            print("2. Check Python path configuration")
            print("3. Verify all dependencies are installed")
            
        except FileNotFoundError as e:
            print()
            print("=" * 60)
            print(Colors.failure("✗ File Not Found"))
            print("=" * 60)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  {Colors.red(str(e))}")
            print(f"\n{Colors.bold('Solutions:')}")
            print("1. Check the wallet file path is correct")
            print("2. Ensure the file exists and is accessible")
            print("3. Try using an absolute path")
            
        except PermissionError as e:
            print()
            print("=" * 60)
            print(Colors.failure("✗ Permission Error"))
            print("=" * 60)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  {Colors.red(str(e))}")
            print(f"\n{Colors.bold('Solutions:')}")
            print("1. Check file permissions")
            print("2. Ensure wallet file is not in use")
            print("3. Try running with appropriate permissions")
            
        except Exception as e:
            print()
            print("=" * 60)
            print(Colors.failure("✗ Unexpected Error"))
            print("=" * 60)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  Type: {Colors.red(type(e).__name__)}")
            print(f"  Message: {Colors.red(str(e))}")
            
            # Try to provide more context for common errors
            error_msg = str(e).lower()
            if "database" in error_msg or "db" in error_msg:
                print(f"\n{Colors.bold('Database Error Troubleshooting:')}")
                print("1. Wallet file may be corrupted")
                print("2. Close Bitcoin Core if running")
                print("3. Check if bsddb3 module is installed")
            elif "decrypt" in error_msg or "crypt" in error_msg:
                print(f"\n{Colors.bold('Encryption Error Troubleshooting:')}")
                print("1. Wallet may not be encrypted")
                print("2. File format may be unsupported")
            else:
                print(f"\n{Colors.bold('General Troubleshooting:')}")
                print("1. Verify the wallet file is valid")
                print("2. Check system resources")
                print("3. Try with a different wallet file")
        
        input("\nPress Enter to continue...")
    
    def pywallet_operations(self):
        """PyWallet operations menu and functionality"""
        self.clear_screen()
        self.print_header()
        
        print("PyWallet Operations")
        print("-" * 50)
        print()
        print("PyWallet provides comprehensive wallet analysis and key extraction:")
        print("• Dump wallet contents (keys, addresses, transactions)")
        print("• Extract private keys from encrypted/unencrypted wallets")
        print("• Export data in multiple formats (JSON, CSV, TXT)")
        print("• Analyze wallet structure and statistics")
        print()
        
        # Get wallet file
        wallet_file = self.get_wallet_file()
        if not wallet_file:
            return
        
        # Ask for passphrase
        passphrase = input("Enter wallet passphrase (or press Enter if not encrypted): ").strip()
        if not passphrase:
            passphrase = None
        
        # Ask for export format
        print("\nAvailable export formats:")
        print("  1. JSON (comprehensive data)")
        print("  2. CSV (keys and addresses)")
        print("  3. TXT (human-readable)")
        print("  4. Display only (no file export)")
        
        while True:
            format_choice = input("\nSelect export format (1-4): ").strip()
            if format_choice in ['1', '2', '3', '4']:
                break
            print("Please select a valid option (1-4)")
        
        format_map = {'1': 'json', '2': 'csv', '3': 'txt', '4': None}
        export_format = format_map[format_choice]
        
        output_file = None
        if export_format:
            default_name = f"wallet_dump.{export_format}"
            output_file = input(f"Output file path (or press Enter for '{default_name}'): ").strip()
            if not output_file:
                output_file = default_name
        
        # Ask about balance information
        include_balance = input("Include balance information? (y/N): ").strip().lower() == 'y'
        
        print(f"\nProcessing wallet with PyWallet...")
        print(f"  File: {wallet_file}")
        if passphrase:
            print("  Passphrase: ***provided***")
        else:
            print("  Passphrase: not provided")
        if output_file:
            print(f"  Export: {output_file} ({export_format.upper()})")
        else:
            print("  Export: display only")
        print()
        
        try:
            # Import pywallet functionality
            print("Loading PyWallet module...")
            sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
            from btcrecover_cli.pywallet_full import ComprehensiveWalletManager
            print(Colors.success("PyWallet module loaded successfully"))
            print()
            
            # Validate wallet file
            print(f"Analyzing wallet file: {wallet_file}")
            if not os.path.exists(wallet_file):
                print(Colors.failure(f"Wallet file not found: {wallet_file}"))
                input("\nPress Enter to continue...")
                return
            
            file_size = os.path.getsize(wallet_file)
            print(f"Wallet file size: {file_size:,} bytes")
            
            if file_size == 0:
                print(Colors.failure("Wallet file is empty"))
                input("\nPress Enter to continue...")
                return
            
            print()
            print("Processing wallet...")
            print("- Opening wallet database")
            print("- Extracting keys and addresses")
            print("- Processing transactions")
            print("- Analyzing wallet structure")
            
            # Initialize comprehensive wallet manager
            wallet_mgr = ComprehensiveWalletManager('bitcoin', verbose=True)
            
            # Run comprehensive wallet dump
            wallet_data = wallet_mgr.dump_wallet(
                wallet_file, 
                passphrase,
                include_balance
            )
            
            # Export data if output file specified
            if output_file and export_format:
                if export_format == 'json':
                    import json
                    with open(output_file, 'w') as f:
                        json.dump(wallet_data, f, indent=2)
                elif export_format == 'csv':
                    self._export_csv(wallet_data, output_file)
                elif export_format == 'txt':
                    self._export_txt(wallet_data, output_file)
            
            if wallet_data:
                print()
                print("=" * 60)
                print(Colors.success("✓ PyWallet analysis completed successfully!"))
                print("=" * 60)
                
                # Display statistics
                stats = wallet_data.get('statistics', {})
                metadata = wallet_data.get('metadata', {})
                
                print(f"\n{Colors.bold('Wallet Analysis Summary:')}")
                print(f"  Wallet Version: {metadata.get('version', 'Unknown')}")
                print(f"  Encrypted: {Colors.green('Yes') if metadata.get('encrypted') else Colors.yellow('No')}")
                print(f"  Total Keys: {Colors.cyan(str(stats.get('total_keys', 0)))}")
                print(f"  Encrypted Keys: {stats.get('encrypted_keys', 0)}")
                print(f"  Unencrypted Keys: {stats.get('unencrypted_keys', 0)}")
                print(f"  Total Addresses: {stats.get('total_addresses', 0)}")
                print(f"  Total Transactions: {stats.get('total_transactions', 0)}")
                
                if output_file and os.path.exists(output_file):
                    print(f"\n{Colors.bold('Export Details:')}")
                    print(f"  File: {Colors.cyan(output_file)}")
                    output_size = os.path.getsize(output_file)
                    print(f"  Size: {output_size:,} bytes")
                    print(f"  Format: {export_format.upper()}")
                    print(f"  Status: {Colors.green('File written successfully')}")
                
                # Show sample of keys if available
                keys = wallet_data.get('keys', [])
                if keys:
                    print(f"\n{Colors.bold('Sample Private Keys:')}")
                    sample_count = min(3, len(keys))
                    for i, key in enumerate(keys[:sample_count]):
                        status = Colors.green('✓') if not key['encrypted'] else Colors.yellow('E')
                        print(f"  {status} {key['address']} - {key['private_key'][:20]}{'...' if len(key['private_key']) > 20 else ''}")
                    
                    if len(keys) > sample_count:
                        print(f"  ... and {len(keys) - sample_count} more keys")
                
                print(f"\n{Colors.bold('Security Notice:')}")
                print("⚠️  Private keys contain sensitive information")
                print("⚠️  Store exported files securely")
                print("⚠️  Delete temporary files after use")
                
            else:
                print()
                print("=" * 60)
                print(Colors.failure("✗ Failed to analyze wallet"))
                print("=" * 60)
                
                print(f"\n{Colors.bold('Possible Issues:')}")
                print("• Wallet file is corrupted or invalid")
                print("• Incorrect passphrase for encrypted wallet")
                print("• Unsupported wallet format or version")
                print("• Database access permissions")
                
        except ImportError as e:
            print()
            print("=" * 60)
            print(Colors.failure("✗ PyWallet Module Error"))
            print("=" * 60)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  {Colors.red(str(e))}")
            print(f"\n{Colors.bold('Solutions:')}")
            print("• Ensure all required modules are installed")
            print("• Check Python environment and dependencies")
            
        except Exception as e:
            print()
            print("=" * 60)
            print(Colors.failure("✗ PyWallet Operation Failed"))
            print("=" * 60)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  Type: {Colors.red(type(e).__name__)}")
            print(f"  Message: {Colors.red(str(e))}")
            
            error_msg = str(e).lower()
            if "passphrase" in error_msg or "password" in error_msg:
                print(f"\n{Colors.bold('Password-Related Troubleshooting:')}")
                print("• Try without passphrase if wallet is not encrypted")
                print("• Verify passphrase is correct")
                print("• Check if wallet uses different encryption method")
            elif "database" in error_msg or "db" in error_msg:
                print(f"\n{Colors.bold('Database Error Troubleshooting:')}")
                print("• Ensure wallet file is not in use by Bitcoin Core")
                print("• Check file permissions and accessibility")
                print("• Verify wallet.dat file is not corrupted")
            else:
                print(f"\n{Colors.bold('General Troubleshooting:')}")
                print("• Verify wallet file path is correct")
                print("• Check available disk space for export")
                print("• Ensure wallet file is a valid Bitcoin Core wallet")
        
        input("\nPress Enter to continue...")
    
    def advanced_pywallet_operations(self):
        """Advanced PyWallet operations menu"""
        self.clear_screen()
        self.print_header()
        
        print("Advanced PyWallet Operations")
        print("=" * 50)
        print()
        print("Select advanced operation:")
        print("  1. Disk scanning and recovery")
        print("  2. Balance checker")
        print("  3. Generate new Bitcoin key")
        print("  4. Web interface (launch browser GUI)")
        print("  5. Multi-network operations (Testnet/Namecoin)")
        print("  6. Back to main menu")
        print()
        
        while True:
            choice = input("Select operation (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                break
            print("Please select a valid option (1-6)")
        
        if choice == '1':
            self._disk_recovery_operation()
        elif choice == '2':
            self._balance_checker_operation()
        elif choice == '3':
            self._key_generation_operation()
        elif choice == '4':
            self._web_interface_operation()
        elif choice == '5':
            self._multi_network_operation()
        elif choice == '6':
            return
    
    def _disk_recovery_operation(self):
        """Disk scanning and recovery operation"""
        self.clear_screen()
        self.print_header()
        
        print("Disk Scanning and Recovery")
        print("-" * 40)
        print()
        print("⚠️  WARNING: Disk scanning requires administrative privileges")
        print("⚠️  This operation can take a long time for large disks")
        print("⚠️  Only scan devices you own or have permission to access")
        print()
        
        # Get device path
        device_path = input("Enter device/file path to scan (e.g., /dev/sda1, C:, file.dat): ").strip()
        if not device_path:
            print("No device path provided")
            input("\nPress Enter to continue...")
            return
        
        # Get scan size
        scan_size_str = input("Enter scan size (e.g., 1GB, 500MB) or press Enter for full scan: ").strip()
        scan_size = None
        if scan_size_str:
            # Parse size
            size_str = scan_size_str.upper()
            multipliers = {'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
            for unit, mult in multipliers.items():
                if size_str.endswith(unit):
                    try:
                        scan_size = int(size_str[:-len(unit)]) * mult
                        break
                    except ValueError:
                        pass
        
        # Output directory
        output_dir = input("Output directory for recovered data (default: 'recovered'): ").strip()
        if not output_dir:
            output_dir = 'recovered'
        
        print(f"\nStarting disk recovery operation...")
        print(f"  Device: {device_path}")
        if scan_size:
            print(f"  Scan size: {scan_size:,} bytes")
        else:
            print(f"  Scan size: Full device")
        print(f"  Output: {output_dir}")
        print()
        
        try:
            from btcrecover_cli.pywallet_full import ComprehensiveWalletManager
            
            wallet_mgr = ComprehensiveWalletManager('bitcoin', verbose=True)
            
            print("Initializing disk scanner...")
            print("Scanning for wallet data patterns...")
            
            results = wallet_mgr.recover_from_device(device_path, scan_size, output_dir)
            
            print()
            print("=" * 60)
            print(Colors.success("✓ Disk recovery completed!"))
            print("=" * 60)
            
            stats = results.get('statistics', {})
            print(f"\n{Colors.bold('Recovery Results:')}")
            print(f"  Total keys found: {stats.get('total_keys_found', 0)}")
            print(f"  Valid keys processed: {stats.get('valid_keys_processed', 0)}")
            print(f"  Unique addresses: {stats.get('unique_addresses', 0)}")
            print(f"  Output directory: {stats.get('output_directory', output_dir)}")
            
            # Show sample recovered keys
            processed_keys = results.get('processed_keys', [])
            if processed_keys:
                print(f"\n{Colors.bold('Sample Recovered Keys:')}")
                sample_count = min(3, len(processed_keys))
                for i, key in enumerate(processed_keys[:sample_count]):
                    print(f"  {Colors.green('✓')} {key['address']} - {key['private_key'][:16]}...")
                
                if len(processed_keys) > sample_count:
                    print(f"  ... and {len(processed_keys) - sample_count} more keys")
            
            print(f"\n{Colors.bold('Next Steps:')}")
            print(f"1. Check the output directory: {output_dir}")
            print("2. Review recovery_results.json for detailed findings")
            print("3. Import recovered keys into a wallet if valid")
            print("4. Check balances of recovered addresses")
            
        except Exception as e:
            print()
            print("=" * 60)
            print(Colors.failure("✗ Disk recovery failed"))
            print("=" * 60)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  {Colors.red(str(e))}")
            
            error_msg = str(e).lower()
            if "permission" in error_msg:
                print(f"\n{Colors.bold('Permission Error Solutions:')}")
                print("• Run as administrator/root for device access")
                print("• Use a file instead of raw device")
                print("• Check device path is correct")
            elif "not found" in error_msg:
                print(f"\n{Colors.bold('Device Not Found Solutions:')}")
                print("• Verify device path spelling")
                print("• Check if device is mounted")
                print("• Try different device notation (e.g., /dev/sda vs sda)")
        
        input("\nPress Enter to continue...")
    
    def _balance_checker_operation(self):
        """Balance checker operation"""
        self.clear_screen()
        self.print_header()
        
        print("Bitcoin Address Balance Checker")
        print("-" * 40)
        print()
        
        # Get address
        address = input("Enter Bitcoin address to check: ").strip()
        if not address:
            print("No address provided")
            input("\nPress Enter to continue...")
            return
        
        # Select network
        print("\nSelect network:")
        print("  1. Bitcoin Mainnet")
        print("  2. Bitcoin Testnet")
        
        while True:
            network_choice = input("Select network (1-2): ").strip()
            if network_choice in ['1', '2']:
                break
            print("Please select 1 or 2")
        
        network = 'bitcoin' if network_choice == '1' else 'testnet'
        
        print(f"\nChecking balance for address: {address}")
        print(f"Network: {network.title()}")
        print("\nQuerying blockchain APIs...")
        
        try:
            from btcrecover_cli.pywallet_full import BalanceChecker
            
            balance_checker = BalanceChecker(network)
            balance_info = balance_checker.check_balance(address)
            
            print()
            print("=" * 50)
            
            if not balance_info.get('error'):
                print(Colors.success("✓ Balance retrieved successfully!"))
                print("=" * 50)
                
                print(f"\n{Colors.bold('Balance Information:')}")
                print(f"  Address: {Colors.cyan(address)}")
                print(f"  Network: {network.title()}")
                print(f"  Balance: {balance_info.get('balance', 0):,} satoshis")
                print(f"  Balance: {balance_info.get('balance_btc', 0):.8f} BTC")
                
                if 'utxo_count' in balance_info:
                    print(f"  UTXOs: {balance_info['utxo_count']}")
                if 'tx_count' in balance_info:
                    print(f"  Transactions: {balance_info['tx_count']}")
                
                print(f"  API Source: {balance_info.get('api', 'Unknown')}")
                
                # Show value in USD (placeholder)
                btc_amount = balance_info.get('balance_btc', 0)
                if btc_amount > 0:
                    print(f"\n{Colors.bold('Note:')} Current BTC price lookup not implemented")
                    print("Use external service to convert BTC to USD/other currencies")
                
            else:
                print(Colors.failure("✗ Failed to retrieve balance"))
                print("=" * 50)
                
                print(f"\n{Colors.bold('Error:')} {balance_info.get('balance', 'API unavailable')}")
                print(f"\n{Colors.bold('Troubleshooting:')}")
                print("• Check address format is correct")
                print("• Verify internet connection")
                print("• Try again later (API may be temporarily down)")
                print("• Use alternative blockchain explorer")
        
        except Exception as e:
            print()
            print("=" * 50)
            print(Colors.failure("✗ Balance check failed"))
            print("=" * 50)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  {Colors.red(str(e))}")
        
        input("\nPress Enter to continue...")
    
    def _key_generation_operation(self):
        """Key generation operation"""
        self.clear_screen()
        self.print_header()
        
        print("Bitcoin Key Generator")
        print("-" * 30)
        print()
        print("⚠️  SECURITY WARNING:")
        print("• Generated keys contain real Bitcoin private keys")
        print("• Store keys securely and never share private keys")
        print("• This is for educational/testing purposes")
        print("• Use proper hardware wallets for significant amounts")
        print()
        
        # Network selection
        print("Select network:")
        print("  1. Bitcoin Mainnet")
        print("  2. Bitcoin Testnet")
        print("  3. Namecoin")
        
        while True:
            network_choice = input("Select network (1-3): ").strip()
            if network_choice in ['1', '2', '3']:
                break
            print("Please select 1, 2, or 3")
        
        network_map = {'1': 'bitcoin', '2': 'testnet', '3': 'namecoin'}
        network = network_map[network_choice]
        
        # Generate key
        try:
            from btcrecover_cli.pywallet_full import ComprehensiveWalletManager
            import secrets
            
            wallet_mgr = ComprehensiveWalletManager(network, verbose=False)
            
            print(f"\nGenerating new {network} key...")
            
            # Generate random private key
            private_key = secrets.token_bytes(32)
            
            # Generate public key and address
            public_key = wallet_mgr.ecc.private_key_to_public_key(private_key)
            public_key_compressed = wallet_mgr.ecc.compress_public_key(public_key)
            
            # Generate addresses
            from btcrecover_cli.bitcoin2john import public_key_to_bc_address
            address_uncompressed = public_key_to_bc_address(public_key)
            address_compressed = public_key_to_bc_address(public_key_compressed)
            
            # Generate WIF
            wif_uncompressed = wallet_mgr._private_key_to_wif(private_key, compressed=False)
            wif_compressed = wallet_mgr._private_key_to_wif(private_key, compressed=True)
            
            print()
            print("=" * 60)
            print(Colors.success("✓ New key generated successfully!"))
            print("=" * 60)
            
            print(f"\n{Colors.bold('Generated Key Information:')}")
            print(f"  Network: {Colors.cyan(network.title())}")
            print(f"\n{Colors.bold('Private Key:')}")
            print(f"  Hex: {Colors.red(binascii.hexlify(private_key).decode())}")
            print(f"  WIF (uncompressed): {Colors.red(wif_uncompressed)}")
            print(f"  WIF (compressed): {Colors.red(wif_compressed)}")
            
            print(f"\n{Colors.bold('Public Keys:')}")
            print(f"  Uncompressed: {binascii.hexlify(public_key).decode()}")
            print(f"  Compressed: {binascii.hexlify(public_key_compressed).decode()}")
            
            print(f"\n{Colors.bold('Addresses:')}")
            print(f"  Uncompressed: {Colors.green(address_uncompressed)}")
            print(f"  Compressed: {Colors.green(address_compressed)}")
            
            # Offer to save to file
            save_to_file = input(f"\n{Colors.bold('Save to file?')} (y/N): ").strip().lower() == 'y'
            
            if save_to_file:
                filename = input("Enter filename (default: 'generated_key.txt'): ").strip()
                if not filename:
                    filename = 'generated_key.txt'
                
                key_data = {
                    'network': network,
                    'private_key_hex': binascii.hexlify(private_key).decode(),
                    'wif_uncompressed': wif_uncompressed,
                    'wif_compressed': wif_compressed,
                    'public_key_uncompressed': binascii.hexlify(public_key).decode(),
                    'public_key_compressed': binascii.hexlify(public_key_compressed).decode(),
                    'address_uncompressed': address_uncompressed,
                    'address_compressed': address_compressed
                }
                
                import json
                with open(filename, 'w') as f:
                    json.dump(key_data, f, indent=2)
                
                print(f"\n{Colors.success('Key saved to:')} {filename}")
            
            print(f"\n{Colors.bold('Security Reminder:')}")
            print("🔒 Never share your private key or WIF")
            print("🔒 Store keys in a secure location")
            print("🔒 Consider using hardware wallets for real funds")
            
        except Exception as e:
            print()
            print("=" * 60)
            print(Colors.failure("✗ Key generation failed"))
            print("=" * 60)
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  {Colors.red(str(e))}")
        
        input("\nPress Enter to continue...")
    
    def _web_interface_operation(self):
        """Web interface operation"""
        self.clear_screen()
        self.print_header()
        
        print("PyWallet Web Interface")
        print("-" * 30)
        print()
        print("The web interface provides a browser-based GUI for wallet operations.")
        print("Features include:")
        print("• Wallet file upload and analysis")
        print("• Balance checking")
        print("• Key generation")
        print("• User-friendly forms and displays")
        print()
        
        # Port selection
        port_input = input("Enter port number (default: 8989): ").strip()
        try:
            port = int(port_input) if port_input else 8989
        except ValueError:
            port = 8989
        
        print(f"\nStarting web interface on port {port}...")
        print("⚠️  Press Ctrl+C to stop the web server")
        print(f"🌐 Open your browser to: http://localhost:{port}")
        print()
        
        try:
            from btcrecover_cli.pywallet_full import ComprehensiveWalletManager
            
            wallet_mgr = ComprehensiveWalletManager('bitcoin', verbose=True)
            web_interface = wallet_mgr.start_web_interface(port)
            
            print(Colors.success(f"✓ Web interface started on http://localhost:{port}"))
            print("\nPress Enter to stop the web server...")
            
            input()  # Wait for user input to stop
            
            print("\nStopping web interface...")
            web_interface.stop_server()
            print(Colors.success("✓ Web interface stopped"))
            
        except Exception as e:
            print()
            print(Colors.failure("✗ Failed to start web interface"))
            print(f"\n{Colors.bold('Error Details:')}")
            print(f"  {Colors.red(str(e))}")
            
            error_msg = str(e).lower()
            if "port" in error_msg or "address" in error_msg:
                print(f"\n{Colors.bold('Port/Address Error Solutions:')}")
                print(f"• Try a different port number")
                print(f"• Check if port {port} is already in use")
                print(f"• Run as administrator if using port < 1024")
        
        input("\nPress Enter to continue...")
    
    def _multi_network_operation(self):
        """Multi-network operations"""
        self.clear_screen()
        self.print_header()
        
        print("Multi-Network Operations")
        print("-" * 30)
        print()
        print("Select network for wallet operations:")
        print("  1. Bitcoin Mainnet (standard)")
        print("  2. Bitcoin Testnet (testing)")
        print("  3. Namecoin (merged-mined altcoin)")
        print("  4. Back to advanced menu")
        print()
        
        while True:
            choice = input("Select network (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                break
            print("Please select 1, 2, 3, or 4")
        
        if choice == '4':
            return
        
        network_map = {'1': 'bitcoin', '2': 'testnet', '3': 'namecoin'}
        network = network_map[choice]
        
        print(f"\nSelected network: {Colors.cyan(network.title())}")
        print("\nAvailable operations:")
        print("  1. Dump wallet for this network")
        print("  2. Check address balance")
        print("  3. Generate key for this network")
        print("  4. Back")
        
        while True:
            op_choice = input("\nSelect operation (1-4): ").strip()
            if op_choice in ['1', '2', '3', '4']:
                break
            print("Please select 1, 2, 3, or 4")
        
        if op_choice == '4':
            return
        elif op_choice == '1':
            # Network-specific wallet dump
            print(f"\nWallet dump for {network} network not yet implemented")
            print("This would analyze wallets specific to the selected network")
        elif op_choice == '2':
            # Network-specific balance check
            print(f"\nBalance check for {network} network")
            if network == 'namecoin':
                print("Namecoin balance checking not yet implemented")
                print("This would use Namecoin-specific APIs")
            else:
                # Use existing balance checker with network
                self._balance_checker_operation()
                return
        elif op_choice == '3':
            # Network-specific key generation
            print(f"\nGenerating key for {network} network...")
            # This would use the key generation with the selected network
            # For now, show placeholder
            print("Network-specific key generation not yet fully implemented")
            print(f"This would generate keys with {network} address format")
        
        input("\nPress Enter to continue...")
    
    def _export_csv(self, wallet_data, output_file):
        """Export wallet data as CSV"""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Address (Uncompressed)', 'Address (Compressed)', 
                'Private Key', 'WIF', 'Encrypted', 'Balance Info'
            ])
            
            for key in wallet_data.get('keys', []):
                writer.writerow([
                    key.get('address_uncompressed', ''),
                    key.get('address_compressed', ''),
                    key.get('private_key', ''),
                    key.get('wif', ''),
                    key.get('encrypted', False),
                    str(key.get('balance_info', {}))
                ])
    
    def _export_txt(self, wallet_data, output_file):
        """Export wallet data as readable text"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Comprehensive Bitcoin Wallet Dump\n")
            f.write("=" * 50 + "\n\n")
            
            # Metadata
            metadata = wallet_data.get('metadata', {})
            f.write("Wallet Information:\n")
            f.write(f"  File: {metadata.get('wallet_file', 'N/A')}\n")
            f.write(f"  Network: {metadata.get('network', 'bitcoin')}\n")
            f.write(f"  Version: {metadata.get('version', 'N/A')}\n")
            f.write(f"  Encrypted: {metadata.get('encrypted', False)}\n")
            f.write("\n")
            
            # Statistics
            stats = wallet_data.get('statistics', {})
            f.write("Statistics:\n")
            f.write(f"  Total Keys: {stats.get('total_keys', 0)}\n")
            f.write(f"  Encrypted Keys: {stats.get('encrypted_keys', 0)}\n")
            f.write(f"  Unencrypted Keys: {stats.get('unencrypted_keys', 0)}\n")
            f.write(f"  Compressed Keys: {stats.get('compressed_keys', 0)}\n")
            f.write(f"  Uncompressed Keys: {stats.get('uncompressed_keys', 0)}\n")
            f.write(f"  Total Addresses: {stats.get('total_addresses', 0)}\n")
            f.write(f"  Total Transactions: {stats.get('total_transactions', 0)}\n")
            if 'total_balance_btc' in stats:
                f.write(f"  Total Balance: {stats['total_balance_btc']:.8f} BTC\n")
            f.write("\n")
            
            # Keys and addresses
            f.write("Private Keys and Addresses:\n")
            f.write("-" * 40 + "\n")
            for i, key in enumerate(wallet_data.get('keys', []), 1):
                f.write(f"\nKey #{i}:\n")
                f.write(f"  Address (Uncompressed): {key.get('address_uncompressed', 'N/A')}\n")
                f.write(f"  Address (Compressed): {key.get('address_compressed', 'N/A')}\n")
                f.write(f"  Private Key: {key.get('private_key', 'ENCRYPTED')}\n")
                f.write(f"  WIF: {key.get('wif', 'N/A')}\n")
                f.write(f"  WIF (Compressed): {key.get('wif_compressed', 'N/A')}\n")
                f.write(f"  Encrypted: {key.get('encrypted', False)}\n")
                if 'balance_info' in key:
                    balance = key['balance_info'].get('balance_btc', 0)
                    f.write(f"  Balance: {balance:.8f} BTC\n")
    
    def view_last_results(self):
        """View the last script execution results."""
        self.clear_screen()
        self.print_header()
        
        if not self.runner.results:
            print("No previous results available.")
            print("Please run some extract scripts first.")
            input("\nPress Enter to continue...")
            return
        
        print("Last Execution Results")
        print("-" * 30)
        
        successful = []
        failed = []
        
        for script_name, result in self.runner.results.items():
            if result["success"] and result["extracted_data"]:
                successful.append((script_name, result))
            else:
                failed.append((script_name, result))
        
        print(f"Summary: {Colors.green(str(len(successful)))} successful, {Colors.red(str(len(failed)))} failed")
        print()
        
        if successful:
            print(Colors.green("Successful extractions:"))
            print(Colors.green("-" * 50))
            for script_name, result in successful:
                print(f"\n{Colors.bold(script_name)}:")
                print(f"  Type: {result['script']['type']}")
                print(f"  Data: {Colors.green(result['extracted_data'])}")
        
        if failed:
            print(Colors.red(f"\nFailed extractions:"))
            print(Colors.red("-" * 50))
            for script_name, result in failed:
                print(f"\n{Colors.bold(script_name)}:")
                print(f"  Type: {result['script']['type']}")
                if result["stderr"]:
                    print(f"  Error: {Colors.red(result['stderr'])}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop."""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                self.list_scripts()
            elif choice == '2':
                self.run_all_scripts()
            elif choice == '3':
                self.run_specific_script()
            elif choice == '4':
                self.generate_john_hash()
            elif choice == '5':
                self.pywallet_operations()
            elif choice == '6':
                self.advanced_pywallet_operations()
            elif choice == '7':
                self.view_last_results()
            elif choice == '8':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Terminal GUI for Bitcoin wallet extract scripts"
    )
    parser.add_argument(
        "--scripts-dir",
        help="Directory containing extract scripts",
        default=None
    )
    parser.add_argument(
        "--wallet-file",
        help="Wallet file to process (runs all scripts non-interactively)",
        default=None
    )
    
    args = parser.parse_args()
    
    # Non-interactive mode
    if args.wallet_file:
        runner = ExtractScriptRunner(args.scripts_dir)
        
        print(f"Running all extract scripts against: {args.wallet_file}")
        print()
        
        def progress_callback(current, total, script_name):
            print(f"[{current}/{total}] {script_name}")
        
        results = runner.run_all_scripts(args.wallet_file, progress_callback)
        
        print("\nResults:")
        print("=" * 50)
        
        successful = 0
        for script_name, result in results.items():
            if result["success"] and result["extracted_data"]:
                successful += 1
                print(Colors.success(script_name))
                print(f"  Data: {Colors.green(result['extracted_data'])}")
                print()
            else:
                print(Colors.failure(script_name))
                if result["stderr"]:
                    print(f"  Error: {Colors.red(result['stderr'])}")
                print()
        
        print(f"Summary: {Colors.green(str(successful))} successful extractions out of {len(results)} scripts")
        return
    
    # Interactive mode
    try:
        gui = TerminalGUI()
        gui.run()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
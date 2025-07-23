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
        print("  5. View last results")
        print("  6. Exit")
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
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.list_scripts()
            elif choice == '2':
                self.run_all_scripts()
            elif choice == '3':
                self.run_specific_script()
            elif choice == '4':
                self.generate_john_hash()
            elif choice == '5':
                self.view_last_results()
            elif choice == '6':
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
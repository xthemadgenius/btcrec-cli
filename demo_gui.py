#!/usr/bin/env python3
"""
Demo script to show the GUI screens
"""

import os
import sys
from extract_gui import TerminalGUI, ExtractScriptRunner

def show_main_menu():
    print("="*70)
    print("  BTC Recovery - Extract Scripts Terminal GUI")
    print("="*70)
    print()
    print("Options:")
    print("  1. List available extract scripts")
    print("  2. Run all scripts against a wallet file")
    print("  3. Run specific script against a wallet file")
    print("  4. View last results")
    print("  5. Exit")
    print()
    print("Enter your choice (1-5): ")

def show_script_list():
    runner = ExtractScriptRunner()
    
    print("="*70)
    print("  BTC Recovery - Extract Scripts Terminal GUI")
    print("="*70)
    print()
    print(f"Found {len(runner.scripts)} extract scripts:")
    print("-" * 70)
    
    for i, script in enumerate(runner.scripts, 1):
        print(f"{i:2d}. {script['name']}")
        print(f"     Type: {script['type']}")
        print(f"     Description: {script['description']}")
        print()

def show_run_all_example():
    print("="*70)
    print("  BTC Recovery - Extract Scripts Terminal GUI")
    print("="*70)
    print()
    print("Run All Extract Scripts")
    print("-" * 30)
    print()
    print("Enter wallet file path (or 'back' to return): /path/to/wallet.dat")
    print()
    print("Running all 14 extract scripts against:")
    print("  /path/to/wallet.dat")
    print()
    print("Progress bar during execution:")
    print("|██████████████████████████████████████████████████| 100.0% - Running: extract-bitcoincore-mkey.py")
    print()

def show_results_example():
    print("Results:")
    print("=" * 70)
    print("✓ extract-bitcoincore-mkey.py: SUCCESS")
    print("✓ extract-multibit-hd-data.py: SUCCESS")
    print("✗ extract-bither-partkey.py: FAILED")
    print("✗ extract-blockchain-main-data.py: FAILED")
    print("✗ extract-electrum-halfseed.py: FAILED")
    print("... (and 9 more)")
    print()
    print("Summary: 2 successful, 12 failed")
    print()
    print("Successful extractions:")
    print()
    print("extract-bitcoincore-mkey.py:")
    print("  Data: YmM65iRhIMReOQ2qaldHbn++T1fYP3nXX5tMHbaA/lqEbLhFk6/1Y5F5x0QJAQBI/maR")
    print()
    print("extract-multibit-hd-data.py:")
    print("  Data: bTU6AAAAAAEAAAAAAAAAYjEFAAkAAAAAIAAAAAkAAAAAAAD3o3a7")
    print()

def show_specific_script_example():
    print("="*70)
    print("  BTC Recovery - Extract Scripts Terminal GUI")
    print("="*70)
    print()
    print("Run Specific Extract Script")
    print("-" * 30)
    print()
    print("Available scripts:")
    print(" 1. extract-bitcoincore-mkey.py (bitcoincore-mkey)")
    print(" 2. extract-multibit-privkey.py (multibit-privkey)")
    print(" 3. extract-electrum-halfseed.py (electrum-halfseed)")
    print(" 4. extract-bither-partkey.py (bither-partkey)")
    print("... (and 10 more)")
    print()
    print("Enter script number (or 'back' to return): 1")
    print()
    print("Enter wallet file path (or 'back' to return): /path/to/wallet.dat")
    print()
    print("Running extract-bitcoincore-mkey.py against:")
    print("  /path/to/wallet.dat")
    print()
    print("Results:")
    print("=" * 50)
    print("✓ SUCCESS: extract-bitcoincore-mkey.py")
    print()
    print("Extracted data:")
    print("YmM65iRhIMReOQ2qaldHbn++T1fYP3nXX5tMHbaA/lqEbLhFk6/1Y5F5x0QJAQBI/maR")

def main():
    print("BTC Recovery Extract Scripts Terminal GUI Demo")
    print("=" * 50)
    print()
    
    print("1. MAIN MENU SCREEN:")
    print("-" * 30)
    show_main_menu()
    
    print("\n" + "="*70)
    print("2. SCRIPT LIST SCREEN:")
    print("-" * 30)
    show_script_list()
    
    print("\n" + "="*70)
    print("3. RUN ALL SCRIPTS SCREEN:")
    print("-" * 30)
    show_run_all_example()
    
    print("\n" + "="*70)
    print("4. RESULTS SCREEN:")
    print("-" * 30)
    show_results_example()
    
    print("\n" + "="*70)
    print("5. RUN SPECIFIC SCRIPT SCREEN:")
    print("-" * 30)
    show_specific_script_example()
    
    print("\n" + "="*70)
    print("COMMAND LINE USAGE:")
    print("-" * 30)
    print("# Interactive mode:")
    print("./btc-extract")
    print()
    print("# Non-interactive mode:")
    print("./btc-extract --wallet-file /path/to/wallet.dat")
    print()
    print("# With custom scripts directory:")
    print("./btc-extract --scripts-dir /custom/path/to/scripts")

if __name__ == "__main__":
    main()
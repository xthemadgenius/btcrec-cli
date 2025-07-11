#!/usr/bin/env python3

"""
Architecture Fix Helper for BTCRecover CLI
This script helps diagnose and fix architecture issues on macOS.
"""

import sys
import platform
import subprocess
import os

def check_architecture():
    """Check system and Python architecture"""
    print("Architecture Diagnostics")
    print("=" * 40)
    
    # System architecture
    system_arch = platform.machine()
    print(f"System Architecture: {system_arch}")
    
    # Python architecture
    python_arch = platform.machine()
    print(f"Python Architecture: {python_arch}")
    
    # Check if on Apple Silicon
    if system_arch == "arm64":
        print("✅ Running on Apple Silicon (ARM64)")
        if python_arch == "x86_64":
            print("⚠️  WARNING: Using x86_64 Python on ARM64 system")
            print("   This can cause architecture mismatch issues")
            return False
        else:
            print("✅ Python architecture matches system")
    else:
        print(f"ℹ️  Running on {system_arch} system")
    
    return True

def find_python_installations():
    """Find available Python installations"""
    print("\nPython Installations")
    print("=" * 40)
    
    pythons = []
    
    # Check common Python locations
    locations = [
        "/usr/bin/python3",
        "/opt/homebrew/bin/python3",
        "/usr/local/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3",
        "/Applications/Python 3.11/python3",
    ]
    
    for location in locations:
        if os.path.exists(location):
            try:
                result = subprocess.run([location, "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    # Check architecture
                    arch_result = subprocess.run([location, "-c", "import platform; print(platform.machine())"], 
                                                capture_output=True, text=True)
                    arch = arch_result.stdout.strip() if arch_result.returncode == 0 else "unknown"
                    
                    pythons.append({
                        "path": location,
                        "version": version,
                        "architecture": arch
                    })
                    print(f"✅ {location}")
                    print(f"   Version: {version}")
                    print(f"   Architecture: {arch}")
            except Exception as e:
                print(f"❌ {location} - Error: {e}")
    
    return pythons

def recommend_solution():
    """Recommend solution based on system"""
    print("\nRecommended Solution")
    print("=" * 40)
    
    system_arch = platform.machine()
    
    if system_arch == "arm64":
        print("For Apple Silicon (M1/M2) Macs:")
        print()
        print("1. Use system Python (recommended):")
        print("   arch -arm64 /usr/bin/python3 -m pip install --user btcrecover-cli")
        print()
        print("2. Or install Homebrew Python:")
        print("   brew install python")
        print("   $(brew --prefix)/bin/python3 -m pip install btcrecover-cli")
        print()
        print("3. Or use Rosetta mode:")
        print("   arch -x86_64 python3 -m pip install btcrecover-cli")
    else:
        print("For Intel Macs:")
        print()
        print("1. Standard installation should work:")
        print("   pip3 install btcrecover-cli")
        print()
        print("2. If issues persist, try:")
        print("   pip3 install --user --no-cache-dir btcrecover-cli")

def test_crypto_import():
    """Test if crypto libraries work"""
    print("\nCrypto Library Test")
    print("=" * 40)
    
    try:
        from Crypto.Cipher import AES
        print("✅ pycryptodome works correctly")
        return True
    except Exception as e:
        print(f"❌ pycryptodome error: {e}")
        return False

def main():
    """Main function"""
    print("BTCRecover CLI Architecture Fix Helper")
    print("=" * 50)
    
    # Check architecture
    arch_ok = check_architecture()
    
    # Find Python installations
    pythons = find_python_installations()
    
    # Test crypto import
    crypto_ok = test_crypto_import()
    
    # Recommend solution
    recommend_solution()
    
    print("\n" + "=" * 50)
    if arch_ok and crypto_ok:
        print("✅ No architecture issues detected")
    else:
        print("⚠️  Architecture issues detected - follow recommendations above")
    
    print("\nFor more help, see INSTALL.md")

if __name__ == "__main__":
    main()
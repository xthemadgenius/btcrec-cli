#!/usr/bin/env python3

"""
Test script to verify BTCRecover CLI installation
"""

import sys
import subprocess
import platform

def test_basic_imports():
    """Test basic Python imports"""
    print("Testing basic Python imports...")
    
    try:
        import argparse
        print("✅ argparse imported successfully")
    except ImportError as e:
        print(f"❌ argparse import failed: {e}")
        return False
    
    try:
        import pathlib
        print("✅ pathlib imported successfully")
    except ImportError as e:
        print(f"❌ pathlib import failed: {e}")
        return False
    
    return True

def test_crypto_imports():
    """Test cryptocurrency-related imports"""
    print("\nTesting cryptocurrency imports...")
    
    try:
        import coincurve
        print("✅ coincurve imported successfully")
    except ImportError as e:
        print(f"❌ coincurve import failed: {e}")
        return False
    
    try:
        from Crypto.Cipher import AES
        print("✅ pycryptodome imported successfully")
    except ImportError as e:
        print(f"❌ pycryptodome import failed: {e}")
        return False
    
    try:
        import google.protobuf
        print("✅ protobuf imported successfully")
    except ImportError as e:
        print(f"❌ protobuf import failed: {e}")
        return False
    
    return True

def test_cli_commands():
    """Test CLI commands"""
    print("\nTesting CLI commands...")
    
    commands = [
        "btcrecover --version",
        "btcrecover --help",
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {cmd} - Success")
            else:
                print(f"❌ {cmd} - Failed with return code {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")
        except subprocess.TimeoutExpired:
            print(f"❌ {cmd} - Timeout")
        except Exception as e:
            print(f"❌ {cmd} - Error: {e}")

def test_direct_scripts():
    """Test direct script access"""
    print("\nTesting direct script access...")
    
    scripts = [
        "btcrecover.py --version",
        "seedrecover.py --version",
    ]
    
    for script in scripts:
        try:
            result = subprocess.run(script.split(), capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {script} - Success")
            else:
                print(f"❌ {script} - Failed with return code {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")
        except subprocess.TimeoutExpired:
            print(f"❌ {script} - Timeout")
        except Exception as e:
            print(f"❌ {script} - Error: {e}")

def main():
    """Main test function"""
    print("BTCRecover CLI Installation Test")
    print("=" * 40)
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print("=" * 40)
    
    all_passed = True
    
    # Test basic imports
    if not test_basic_imports():
        all_passed = False
    
    # Test crypto imports
    if not test_crypto_imports():
        all_passed = False
    
    # Test CLI commands
    test_cli_commands()
    
    # Test direct scripts
    test_direct_scripts()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ All critical tests passed!")
    else:
        print("❌ Some critical tests failed!")
    
    print("\nInstallation test complete.")

if __name__ == "__main__":
    main()
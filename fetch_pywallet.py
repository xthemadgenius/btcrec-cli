#!/usr/bin/env python3
"""
Script to fetch the original pywallet.py from GitHub
"""
import requests
import os

def fetch_original_pywallet():
    """Download original pywallet.py from GitHub"""
    url = "https://raw.githubusercontent.com/jackjack-jj/pywallet/master/pywallet.py"
    
    try:
        print("Fetching original pywallet.py from GitHub...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        output_path = "original_pywallet.py"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✓ Successfully downloaded to {output_path}")
        print(f"File size: {len(response.text):,} characters")
        
        # Show first few lines to verify
        lines = response.text.split('\n')[:10]
        print("\nFirst 10 lines:")
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line}")
        
        return output_path
        
    except Exception as e:
        print(f"✗ Failed to fetch pywallet.py: {e}")
        return None

if __name__ == "__main__":
    fetch_original_pywallet()
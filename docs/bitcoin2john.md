# Bitcoin2John Integration

The btcrec-cli now includes comprehensive bitcoin2john functionality for converting Bitcoin wallet.dat files to John the Ripper hash format, with full support for legacy wallets dating back to 2008.

## Overview

The bitcoin2john tool extracts encryption information from Bitcoin Core wallet.dat files and converts it to a format suitable for password cracking with John the Ripper. This comprehensive implementation supports:

- **Modern Bitcoin Core wallets** (2010-present)
- **Legacy Bitcoin wallets** (2008-2009) - crucial for early adopters
- **Various database formats** and encryption methods
- **Raw device/disk reading** for damaged wallet recovery
- **Comprehensive record type parsing** for maximum compatibility

This is essential for users with 16-year-old Bitcoin wallets who need password recovery support.

## Usage

### CLI Usage

#### Using the btcrecover command:
```bash
# Generate hash to stdout
btcrecover bitcoin2john wallet.dat

# Generate hash to file
btcrecover bitcoin2john wallet.dat -o wallet.hash
```

#### Using the direct script:
```bash
# Generate hash to stdout
bitcoin2john.py wallet.dat

# Generate hash to file  
bitcoin2john.py wallet.dat -o wallet.hash

# Verbose output
bitcoin2john.py wallet.dat -v

# Legacy mode for very old wallets (2008-2010)
bitcoin2john.py wallet.dat --legacy-mode -v

# Full comprehensive mode
bitcoin2john.py wallet.dat --legacy-mode -v -o old_wallet.hash
```

### GUI Usage

The bitcoin2john functionality is also available through the terminal GUI:

```bash
python3 extract_gui.py
```

Then select option 4: "Generate John the Ripper hash (bitcoin2john)"

## Output Format

The tool generates hashes in the John the Ripper format:

```
wallet.dat:$bitcoin$48$encrypted_key$8$salt$iterations$48$encrypted_private_key$derivation_method
```

## Requirements

- Bitcoin Core wallet.dat file (encrypted)
- Python 3.9+
- bsddb3 or bsddb package
- ecdsa package (optional, for enhanced legacy wallet support)

## Legacy Wallet Support

This implementation provides comprehensive support for Bitcoin wallets created as early as 2008-2009, which is crucial for early Bitcoin adopters. Legacy features include:

- **Early database formats** from the original Bitcoin client
- **Raw device reading** for recovering from damaged disks
- **Comprehensive record parsing** for all wallet database record types
- **Legacy key formats** and cryptographic methods
- **Old transaction and pool record support**

For very old wallets, use the `--legacy-mode` flag for maximum compatibility.

## Troubleshooting

### "No encrypted keys found in wallet"
This means the wallet file is either:
- Not encrypted (no password set)
- Corrupted
- Not a valid Bitcoin Core wallet.dat file

### "Database error" 
- Ensure the wallet.dat file is not in use by Bitcoin Core
- Check file permissions
- Verify the file is a valid Berkeley DB file

## Integration with John the Ripper

After generating the hash, you can use it with John the Ripper:

```bash
# Basic password cracking
john wallet.hash

# Using a wordlist
john --wordlist=passwords.txt wallet.hash

# Using rules
john --rules --wordlist=passwords.txt wallet.hash
```

## Security Note

This tool should only be used on wallet files that you legitimately own. It is designed for legitimate password recovery purposes only.
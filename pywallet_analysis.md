# PyWallet Analysis for GUI Integration

## Overview
PyWallet is a comprehensive Bitcoin wallet recovery and management tool written in Python. It's designed for wallet.dat file manipulation, private key recovery, and blockchain data management.

## Main Operations

### 1. Wallet Dumping
- **Function**: Extract private keys and addresses from wallet.dat files
- **Purpose**: Backup and recovery of wallet contents
- **Output**: JSON format with all wallet data

### 2. Key Recovery
- **Function**: Scan disk drives/partitions for deleted wallet keys
- **Purpose**: Recover lost or accidentally deleted private keys
- **Method**: Byte-level disk scanning for key patterns

### 3. Wallet Management
- **Function**: Import/export keys, merge wallets, create transactions
- **Purpose**: Advanced wallet operations and maintenance

### 4. Web Interface
- **Function**: Browser-based GUI for wallet operations
- **Purpose**: User-friendly access to wallet functions

## Key Command-Line Arguments

### Basic Operations
- `--dumpwallet` - Dump wallet contents in JSON format
- `--dumpwithbalance` - Include address balances in dump
- `--web` - Launch web interface
- `--version` - Show version information
- `--help` - Display help information

### Wallet Specification
- `--datadir=DATADIR` - Specify wallet directory (default: Bitcoin data dir)
- `--wallet=WALLETFILE` - Specify wallet filename (default: wallet.dat)
- `--passphrase=PASSPHRASE` - Password for encrypted wallets

### Recovery Options
- `--recover` - Enable key recovery mode
- `--recov_device=DEVICE` - Device/file to scan (e.g., /dev/sda1, C:, file.dat)
- `--recov_size=SIZE` - Amount of data to scan (e.g., 20Mo, 50Gio)
- `--recov_outputdir=DIR` - Output directory for recovered keys

### Network Options
- `--testnet` - Use Bitcoin testnet
- `--otherversion=VERSION` - Specify wallet version

## Usage Examples

### Basic Wallet Dump
```bash
python pywallet.py --dumpwallet --datadir=./ --wallet=wallet.dat
```

### Encrypted Wallet Dump with Balance
```bash
python pywallet.py --dumpwallet --dumpwithbalance --passphrase=mypassword
```

### Key Recovery from Disk
```bash
python pywallet.py --recover --recov_device=/dev/sda1 --recov_size=10Gio --recov_outputdir=./recovered
```

### Web Interface
```bash
python pywallet.py --web
```

## Main Functions for GUI Integration

### 1. Wallet Reading Functions
- `read_wallet(filename, passphrase=None)` - Parse wallet.dat file
- `parse_wallet_data(data)` - Extract wallet information
- `decrypt_wallet(data, passphrase)` - Decrypt encrypted wallets

### 2. Key Management Functions
- `extract_keys(wallet_data)` - Get private keys from wallet
- `import_key(key, wallet)` - Add key to wallet
- `export_keys(wallet, format)` - Export keys in various formats

### 3. Recovery Functions
- `recover_keys(device, size, output_dir)` - Scan for deleted keys
- `scan_device(device, patterns)` - Low-level disk scanning
- `validate_recovered_keys(keys)` - Verify recovered key integrity

### 4. Utility Functions
- `get_address_from_key(private_key)` - Generate Bitcoin address
- `check_key_validity(key)` - Validate private key format
- `get_balance(address)` - Check address balance (if API available)

## Dependencies

### Required
- **Python 2.7** (Not Python 3 compatible)
- **bsddb/bsddb3** - Berkeley DB interface for wallet.dat parsing
- **hashlib** - Cryptographic hash functions
- **json** - JSON data handling

### Optional
- **ecdsa** - Elliptic curve cryptography (can use built-in implementation)
- **Crypto.Cipher** - Advanced encryption operations
- **twisted** - For web interface functionality

## GUI Integration Recommendations

### Core Features to Expose
1. **Wallet File Selection** - File browser for wallet.dat files
2. **Passphrase Input** - Secure password entry for encrypted wallets
3. **Dump Wallet** - Extract and display all keys/addresses
4. **Export Options** - Save keys in various formats (JSON, CSV, text)
5. **Recovery Mode** - Drive/file selection for key recovery
6. **Progress Indicators** - Show scanning/processing progress

### Advanced Features
1. **Balance Checking** - Display address balances
2. **Key Validation** - Verify private key integrity
3. **Multiple Wallet Support** - Handle multiple wallet files
4. **Testnet Support** - Switch between mainnet/testnet

### Security Considerations
1. **Secure Memory Handling** - Clear sensitive data from memory
2. **Passphrase Protection** - Secure password storage/handling
3. **File Permissions** - Proper access controls for wallet files
4. **Backup Warnings** - Warn users about backup importance

### User Experience Features
1. **Drag & Drop** - Easy wallet file loading
2. **Progress Bars** - Visual feedback for long operations
3. **Error Handling** - Clear error messages and recovery options
4. **Export Formats** - Multiple output options (PDF, encrypted files)
5. **Recovery Wizard** - Step-by-step recovery process

## Limitations and Considerations
- **Python 2.7 Only** - No Python 3 support
- **Berkeley DB Dependency** - Required for wallet.dat parsing
- **Disk Scanning Speed** - Recovery operations can be time-intensive
- **Balance API Limits** - External API dependency for balance checking
- **Security Risks** - Handles sensitive cryptographic data

This analysis provides the foundation for integrating pywallet functionality into a modern GUI application while maintaining security and usability.
# BTCRecover CLI Installation Guide

## Overview

BTCRecover CLI is a professional command-line interface for the BTCRecover cryptocurrency wallet recovery tool. This guide provides comprehensive installation instructions for all supported platforms.

## Quick Start

### For Most Users (Recommended)

```bash
# Install using pip
pip install btcrecover-cli

# Or install from source
git clone https://github.com/3rdIteration/btcrecover.git
cd btcrecover
pip install -e .
```

### For Advanced Users

```bash
# Install with full dependencies for maximum compatibility
pip install -r requirements-full.txt
pip install -e .
```

## Detailed Installation Instructions

### Prerequisites

- **Python 3.9 or higher** (Python 3.11+ recommended)
- **pip** (Python package manager)
- **git** (for source installation)

### Platform-Specific Instructions

#### macOS

##### Option 1: Using Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install BTCRecover CLI
pip3 install btcrecover-cli
```

##### Option 2: Using System Python (Apple Silicon Macs)

If you encounter architecture issues on Apple Silicon (M1/M2) Macs:

```bash
# Use system Python to avoid architecture conflicts
arch -arm64 /usr/bin/python3 -m pip install --user btcrecover-cli

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

##### Option 3: Source Installation

```bash
# Clone the repository
git clone https://github.com/3rdIteration/btcrecover.git
cd btcrecover

# Create virtual environment
python3 -m venv btcrecover-env
source btcrecover-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install CLI
pip install -e .
```

#### Linux

##### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git

# Install BTCRecover CLI
pip3 install --user btcrecover-cli

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

##### CentOS/RHEL/Fedora

```bash
# Install Python and pip
sudo dnf install python3 python3-pip git  # Fedora
# OR
sudo yum install python3 python3-pip git  # CentOS/RHEL

# Install BTCRecover CLI
pip3 install --user btcrecover-cli

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

##### Arch Linux

```bash
# Install Python and pip
sudo pacman -S python python-pip git

# Install BTCRecover CLI
pip install --user btcrecover-cli

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows

##### Option 1: Using Python from python.org

1. Download Python from https://python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation
3. Open Command Prompt or PowerShell
4. Install BTCRecover CLI:

```cmd
pip install btcrecover-cli
```

##### Option 2: Using Windows Package Manager

```powershell
# Install Python using winget
winget install Python.Python.3.11

# Install BTCRecover CLI
pip install btcrecover-cli
```

##### Option 3: Using Chocolatey

```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python
choco install python

# Install BTCRecover CLI
pip install btcrecover-cli
```

## Virtual Environment Installation (Recommended)

Using a virtual environment isolates BTCRecover CLI from your system Python and prevents conflicts:

```bash
# Create virtual environment
python3 -m venv btcrecover-env

# Activate virtual environment
# On macOS/Linux:
source btcrecover-env/bin/activate
# On Windows:
btcrecover-env\Scripts\activate

# Install BTCRecover CLI
pip install btcrecover-cli

# When done, deactivate
deactivate
```

## Verification

After installation, verify everything works:

```bash
# Check version
btcrecover --version

# Check direct script access
btcrecover.py --version
seedrecover.py --version

# View help
btcrecover --help
btcrecover.py --help
```

## Usage Examples

### Direct Script Access (Matches Official Documentation)

```bash
# Password recovery
btcrecover.py --wallet wallet.dat --passwordlist passwords.txt

# Seed recovery
seedrecover.py --mnemonic "abandon abandon abandon..." --addr 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2

# Address database creation
create-address-db.py --dbfilename addresses.db --addresses-file addresses.txt
```

### Convenience Commands

```bash
# Password recovery
btcrecover password --wallet wallet.dat --passwordlist passwords.txt

# Seed recovery
btcrecover seed --mnemonic "abandon abandon abandon..." --addr 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2

# Address database creation
btcrecover create-db --dbfilename addresses.db --addresses-file addresses.txt
```

## Troubleshooting

### Common Issues

#### 1. Architecture Mismatch (Apple Silicon Macs)

**Error**: `OSError: Cannot load native module 'Crypto.Util._cpuid_c'`

**Solution**:
```bash
# Uninstall existing packages
pip uninstall -y pycryptodome coincurve

# Reinstall with system Python
arch -arm64 /usr/bin/python3 -m pip install --user --no-cache-dir pycryptodome coincurve

# Or use Homebrew Python
brew install python
$(brew --prefix)/bin/python3 -m pip install btcrecover-cli
```

#### 2. Permission Issues

**Error**: `Permission denied` when installing

**Solution**:
```bash
# Install to user directory
pip install --user btcrecover-cli

# Or use virtual environment
python3 -m venv btcrecover-env
source btcrecover-env/bin/activate
pip install btcrecover-cli
```

#### 3. Command Not Found

**Error**: `btcrecover: command not found`

**Solution**:
```bash
# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or find installation location
python3 -m pip show -f btcrecover-cli
```

#### 4. ImportError Issues

**Error**: `ImportError: No module named 'Crypto'`

**Solution**:
```bash
# Install missing dependencies
pip install -r requirements-full.txt

# Or install individually
pip install pycryptodome coincurve protobuf
```

#### 5. SSL Certificate Issues

**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**:
```bash
# Update certificates
pip install --upgrade certifi

# Or use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org btcrecover-cli
```

### Platform-Specific Issues

#### macOS

- **Issue**: Command line tools not found
- **Solution**: `xcode-select --install`

#### Linux

- **Issue**: Missing development headers
- **Solution**: `sudo apt install python3-dev build-essential` (Ubuntu/Debian)

#### Windows

- **Issue**: Visual C++ build tools missing
- **Solution**: Install Microsoft Visual C++ Build Tools

### Performance Issues

If you experience slow performance:

```bash
# Install with full dependencies for GPU acceleration
pip install -r requirements-full.txt

# Check OpenCL support
btcrecover.py --opencl-info

# Check GPU support
btcrecover.py --list-gpus
```

## Getting Help

- **Official Documentation**: https://btcrecover.readthedocs.io/
- **GitHub Issues**: https://github.com/3rdIteration/btcrecover/issues
- **YouTube Tutorials**: https://www.youtube.com/playlist?list=PL7rfJxwogDzmd1IanPrmlTg3ewAIq-BZJ

## Advanced Configuration

### Custom Installation Path

```bash
# Install to custom location
pip install --target /custom/path btcrecover-cli

# Add to Python path
export PYTHONPATH="/custom/path:$PYTHONPATH"
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/3rdIteration/btcrecover.git
cd btcrecover

# Create development environment
python3 -m venv dev-env
source dev-env/bin/activate

# Install in development mode
pip install -e .

# Install additional development dependencies
pip install -r requirements-full.txt
```

## Security Considerations

1. **Always work with wallet file copies**
2. **Use offline systems when possible**
3. **Verify checksums of downloaded files**
4. **Keep recovery phrases secure**
5. **Use virtual environments to isolate dependencies**

## Uninstallation

```bash
# Uninstall BTCRecover CLI
pip uninstall btcrecover-cli

# Remove virtual environment (if used)
rm -rf btcrecover-env

# Remove user installations
pip uninstall --user btcrecover-cli
```

## License

BTCRecover CLI is licensed under the GNU General Public License v2.0. See the LICENSE file for details.
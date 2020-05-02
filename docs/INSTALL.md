## *btcrecover* Installation ##

Just download the latest version from <https://github.com/3rdIteration/btcrecover/archive/master.zip> and unzip it to a location of your choice. There’s no installation procedure for *btcrecover* itself, however there are additional requirements below depending on your operating system and the wallet type you’re trying to recover.

### Wallet Installation Requirements ###

Locate your wallet type in the list below, and follow the instructions for only the sections listed next to your wallet.

**Note** that for Armory wallets, you must have Armory 0.92.x or later installed on the computer where you run *btcrecover*.

 * Armory 0.91.x or earlier - unsupported, please upgrade Armory first
 * Armory 0.92.x on Windows -[Python 3.8](#python-38)(x86)
 * Armory 0.93+ on Windows - [Python 3.8](#python-38) **64-bit** (x86-64)
 * Armory 0.92+ on Linux - no additional requirements
 * Armory 0.92+ on OS X - some versions of Armory may not work correctly on OS X, if in doubt use version 0.95.1
 * Bitcoin Unlimited/Classic/XT/Core - optional: [PyCryptoDome](#pycryptodome)
 * MultiBit Classic - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * MultiBit HD - [Python 3.8](#python-38), optional: [PyCryptoDome](#pycryptodome)
 * Electrum (1.x or 2.x) - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * Electrum 2.8+ fully encrypted wallets - [Python 3.8](#python-38), [coincurve](Seedrecover_Quick_Start_Guide.md#installation), optional: [PyCryptoDome](#pycryptodome)
 * BIP-39 Bitcoin passphrases (e.g. TREZOR) - [Python 3.8](#python-38), [coincurve](Seedrecover_Quick_Start_Guide.md#installation)
 * BIP-39 Ethereum passphrases (e.g. TREZOR) - [Python 3.8](#python-38), [PyCryptoDome](#pycryptodome) [coincurve](Seedrecover_Quick_Start_Guide.md#installation)
 * Hive for OS X - [Python 3.8](#python-38), [Google protobuf](#google-protocol-buffers), optional: [PyCryptoDome](#pycryptodome)
 * mSIGNA (CoinVault) - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * Blockchain.info - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * Bitcoin Wallet for Android/BlackBerry backup - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * Bitcoin Wallet for Android/BlackBerry spending PIN - [Python 3.8](#python-38), [scrypt](#scrypt), [Google protobuf](#google-protocol-buffers), optional: [PyCryptoDome](#pycryptodome)
 * KnC Wallet for Android backup - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * Bither - [Python 3.8](#python-38), [coincurve](Seedrecover_Quick_Start_Guide.md#installation), optional: [PyCryptoDome](#pycryptodome)
 * Litecoin-Qt - [Python 3.8](#python-38),  optional: [PyCryptoDome](#pycryptodome)
 * Electrum-LTC - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * Litecoin Wallet for Android - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * Dogecoin Core - [Python 3.8](#python-38),  optional: [PyCryptoDome](#pycryptodome)
 * MultiDoge - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)
 * Dogecoin Wallet for Android - [Python 3.8](#python-38), recommended: [PyCryptoDome](#pycryptodome)


----------


### Python 3.8 ###

##### Windows #####

Visit the Python download page here: <https://www.python.org/downloads/windows/>, and click the link for the latest **Python 3.8** release near the top of the page under the heading *Python Releases for Windows*. Download and run either the `Windows x86 MSI installer` for the 32-bit version of Python, or the `Windows x86-64 MSI installer` for the 64-bit one (for Armory wallets, be sure to choose the correct one as noted above). Modern PCs should use the 64-bit version, however if you're unsure which one is compatible with your PC, choose the 32-bit one.

_**When installing Python in Windows, be sure to select to "Add Python 3.8 to PATH" on the first screen of the installer...**_

##### Linux #####

Most modern distributions include Python 3 pre-installed. Older Linux distributions will include Python2, so you will need to install python3.

Some Linux distributions do not include the bsddb3 (Berkeley DB) Python module. This is usually not a problem, however if you encounter a `master key #1 not found` error, it might be resolved by installing the bsddb3 module via PIP.

##### OS X #####

Since OS X includes an older version of Python 2, it's strongly recommended that you install the latest version. Doing so will not affect the older OS X version, the new one will be installed in a different place from the existing one.

To install the latest version, visit the Python download page here: <https://www.python.org/downloads/mac-osx/>, and click the link for the latest **Python 3** release. Download and open either the `Mac OS X 64-bit/32-bit installer` for OS X 10.6 and later (most people will want this one), or the `Mac OS X 32-bit i386/PPC installer` for OS X 10.5.

If you have any Terminal windows open, close them after the installation completes to allow the new version to go into effect.

If (and only if) you decide *not* to install the latest version of Python 3, you will need to manually install `pip` if you need to install any of the other requirements below:

        curl https://bootstrap.pypa.io/get-pip.py | sudo python


### PyCryptoDome ###

With the exception of Ethereum wallets, PyCryptoDome is not strictly required for any wallet, however it offers a 20x speed improvement for wallets that tag it as recommended in the list above.

##### Windows #####

PyCryptoDome support is provided via the pycryptodome module. This can be installed via PIP.

##### Linux #####

Many distributions include PyCrypto pre-installed, check your distribution’s package management system to see if it is available (it is often called “python3-pycryptodome”). If not, try installing it from PyPI, for example on Debian-like distributions (including Ubuntu), if this doesn't work:

    sudo apt-get install python3-pycryptodome

then try this instead:

    sudo apt-get install python3-pip
    sudo pip3 install pycryptodome

##### OS X #####

 1. Open a terminal window (open the Launchpad and search for "terminal"). Type this and then choose `Install` to install the command line developer tools:

        xcode-select --install

 2. Type this to install PyCryptoDome

        sudo pip3 install pycryptodome


### Google Protocol Buffers ###

##### Windows #####

Open a command prompt window, and type this to install Google Protocol Buffers:

    pip3 install protobuf

##### Linux #####

Install the Google's Python protobuf library, for example on Debian-like distributions (including Ubuntu), open a terminal window and type this:

    sudo apt-get install python3-pip
    sudo pip3 install protobuf

##### OS X #####

 1. Open a terminal window (open the Launchpad and search for "terminal"). Type this and then choose `Install` to install the command line developer tools:

        xcode-select --install

 2. Type this to install Google Protocol Buffers:

        sudo pip3 install protobuf

----------


### Windows GPU acceleration for Bitcoin Unlimited/Classic/XT/Core, Armory, or Litecoin-Qt ### 

### Totally Untested for Python3, docco below obselete...

 1. Download the latest version of PyOpenCL for OpenCL 1.2 / Python 2.7, either the 32-bit version or the 64-bit version to match the version of Python you installed, from here: <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl>. For best compatibility, be sure to select a version for OpenCL 1.2 *and no later* (look for "cl12" in the file name, and also look for "27" to match Python 2.7).

    As of this writing, the 32-bit and 64-bit versions are named respectively:

        pyopencl‑2018.1.1+cl12‑cp27‑cp27m‑win32.whl
        pyopencl‑2018.1.1+cl12‑cp27‑cp27m‑win_amd64.whl

 2. Open a command prompt window, and type this to install PyOpenCL and its dependencies:

        cd %USERPROFILE%\Downloads
        C:\Python27\Scripts\pip install pyopencl‑2018.1.1+cl12‑cp27‑cp27m‑win_amd64.whl

    Note that you may need to change either the directory (on the first line) or the filename (on the second) depending on the filename you downloaded and its location.

[PyCryptoDome](#pycryptodome) is also recommended for Bitcoin Unlimited/Classic/XT/Core or Litecoin-Qt wallets for a 2x speed improvement.

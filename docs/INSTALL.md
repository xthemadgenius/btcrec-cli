## *btcrecover* Installation ##

Just download the latest version from <https://github.com/3rdIteration/btcrecover/archive/master.zip> and unzip it to a location of your choice. There’s no installation procedure for *btcrecover* itself, however there are additional requirements below depending on your operating system and the wallet type you’re trying to recover.

### Wallet Installation Requirements ###

Locate your wallet type in the list below, and follow the instructions for only the sections listed next to your wallet.

 * Bitcoin Core - optional: [PyCryptoDome](#pycryptodome)
 * MultiBit Classic - recommended: [PyCryptoDome](#pycryptodome)
 * MultiBit HD - optional: [PyCryptoDome](#pycryptodome)
 * Electrum (1.x or 2.x) - recommended: [PyCryptoDome](#pycryptodome)
 * Electrum 2.8+ fully encrypted wallets - [coincurve](Seedrecover_Quick_Start_Guide.md#installation), optional: [PyCryptoDome](#pycryptodome)
 * BIP-39 Bitcoin passphrases (e.g. TREZOR) - [coincurve](Seedrecover_Quick_Start_Guide.md#installation)
 * BIP-39 Ethereum passphrases (e.g. TREZOR) - [PyCryptoDome](#pycryptodome) [coincurve](Seedrecover_Quick_Start_Guide.md#installation)
 * Hive for OS X - [Google protobuf](#google-protocol-buffers), optional: [PyCryptoDome](#pycryptodome)
 * mSIGNA (CoinVault) - recommended: [PyCryptoDome](#pycryptodome)
 * Blockchain.info - recommended: [PyCryptoDome](#pycryptodome)
 * Bitcoin Wallet for Android/BlackBerry backup - recommended: [PyCryptoDome](#pycryptodome)
 * Bitcoin Wallet for Android/BlackBerry spending PIN - [scrypt](#scrypt), [Google protobuf](#google-protocol-buffers), optional: [PyCryptoDome](#pycryptodome)
 * KnC Wallet for Android backup - recommended: [PyCryptoDome](#pycryptodome)
 * Bither - [coincurve](Seedrecover_Quick_Start_Guide.md#installation), optional: [PyCryptoDome](#pycryptodome)
 * Litecoin-Qt -  optional: [PyCryptoDome](#pycryptodome)
 * Electrum-LTC - recommended: [PyCryptoDome](#pycryptodome)
 * Litecoin Wallet for Android - recommended: [PyCryptoDome](#pycryptodome)
 * Dogecoin Core -  optional: [PyCryptoDome](#pycryptodome)
 * MultiDoge - recommended: [PyCryptoDome](#pycryptodome)
 * Dogecoin Wallet for Android - recommended: [PyCryptoDome](#pycryptodome)


----------


### Python ###

**Note:** Only Python 3.6 and later are officially supported... BTCRecover is automatically tested with all supported Python versions (3.6, 3.7, 3.8) on all supported environments (Windows, Linux, Mac), so you can be sure that both BTCRecover and all required packages will work correctly. Some features of BTCRecover may work on earlier versions of Python, your best bet is to use run-all-tests.py to see what works and what doesn't...

Once both Python3 and PIP have been installed, you can automatically install all the requirements for all features of BTCRecover with the command:

`pip3 install -r requirements.txt`

##### Windows #####

Visit the Python download page here: <https://www.python.org/downloads/windows/>, and click the link for the latest **Python 3.8** release near the top of the page under the heading *Python Releases for Windows*. Download and run either the `Windows x86 MSI installer` for the 32-bit version of Python, or the `Windows x86-64 MSI installer` for the 64-bit one. Modern PCs should use the 64-bit version, however if you're unsure which one is compatible with your PC, choose the 32-bit one.

_**When installing Python in Windows, be sure to select to "Add Python 3.8 to PATH" on the first screen of the installer...**_

##### Linux #####

Most modern distributions include Python 3 pre-installed. Older Linux distributions will include Python2, so you will need to install python3.

If you are using SeedRecover, you will also need to install tkinter (python3-tk) if you want to use the default GUI popups for seedrecover. (Command line use will work find without this package)

Some distributions of Linux will bundle this with Python3, but for others like Ubuntu, you will need to manually install the tkinter module.

You can install this with the command: `sudo apt install python3-tk`

##### MacOS #####

Since MacOS 10.13 (High Sierra), both Python3 and PIP come bundled with MacOS. (I don't have a MacOS to test this but I believe this is the case)

If you run into issues, you can download and install the latest python3 release from python.org

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


### Windows GPU acceleration ### 
For Bitcoin Core Password Recovery (Also works for derived forks)

 1. Download the latest version of PyOpenCL for OpenCL 1.2 and Python 3, either the 32-bit version or the 64-bit version to match the version of Python you installed, from here: <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl>. For best compatibility, be sure to select a version for OpenCL 1.2 *and no later* (look for "cl12" in the file name, and also look for the numbers to maych your python version (eg: "38" to match Python 3.8).

    As of this writing, the 32-bit and 64-bit versions, for OpenCL 1.2 and Python 3.8 are named respectively:

        pyopencl‑2020.1+cl12‑cp38‑cp38‑win_amd64.whl
        pyopencl‑2020.1+cl12‑cp38‑cp38‑win32.whl

 2. Open a command prompt window, and type this to install PyOpenCL and its dependencies: (Assuming Python3.8 in a 64bit environment)

        pip3 install pyopencl‑2020.1+cl12‑cp38‑cp38‑win_amd64.whl

    Note that you may need to change either the directory (on the first line) or the filename (on the second) depending on the filename you downloaded and its location.

[PyCryptoDome](#pycryptodome) is also recommended for Bitcoin Core or Litecoin-Qt wallets for a 2x speed improvement.

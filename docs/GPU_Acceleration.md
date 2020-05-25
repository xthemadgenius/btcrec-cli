## *btcrecover* GPU Acceleration Guide ##

*btcrecover* includes experimental support for using one or more graphics cards or dedicated accelerator cards to increase search performance. This can offer on the order of *2000x* better performance with Bitcoin Unlimited/Classic/XT/Core or altcoin wallets when enabled and correctly tuned. 

In order to use this feature, you must have a card and drivers which support OpenCL (most AMD and NVIDIA cards and drivers already support OpenCL on Windows), and you must install the required Python libraries as described in the [Windows GPU acceleration](INSTALL.md#windows-gpu-acceleration) section of the Installation Guide. GPU acceleration should also work on Linux and OS X, however instructions for installing the required Python libraries are not currently included in this tutorial.

Due to its experimental status, it's highly recommended that you run the GPU unit tests before running it with a wallet. 

    python3 -m btcrecover.test.test_passwords -v GPUTests

Assuming the tests do not fail, GPU support can be enabled by adding the `--enable-gpu` option to the command line. There are other additional options, specifically `--global-ws` and `--local-ws`, which should also be provided along with particular values to improve the search performance. Unfortunately, the exact values for these options can only be determined by trial and error, as detailed below.

### GPU performance tuning for Bitcoin Core and derived altcoin wallets ###

A good starting point for these wallets is:

    python3 btcrecover.py --wallet ./btcrecover/test/test-wallets/bitcoincore-wallet.dat --performance --enable-gpu --global-ws 4096 --local-ws 256

The `--performance` option tells *btcrecover* to simply measure the performance until Ctrl-C is pressed, and not to try testing any particular passwords. You will still need a wallet file (or an `--extract-data` option) for performance testing. After you you have a baseline from this initial test, you can try different values for `--global-ws` and `--local-ws` to see if they improve or worsen performance.

Finding the right values for `--global-ws` and `--local-ws` can make a 10x improvement, so it's usually worth the effort.

Generally when testing, you should increase or decrease these two values by powers of 2, for example you should increase or decrease them by 128 or 256 at a time. It's important to note that `--global-ws` must always be evenly divisible by `--local-ws`, otherwise *btcrecover* will exit with an error message.

Although this procedure can be tedious, with larger tokenlists or passwordlists it can make a significant difference.

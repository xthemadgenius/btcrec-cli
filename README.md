# *btcrecover* [![Build Status](https://api.travis-ci.org/3rdIteration/btcrecover.svg?branch=p2wpkh-p2sh)](https://travis-ci.org/3rdIteration/btcrecover) ![license](https://img.shields.io/badge/license-GPLv2-blue.svg) #

*btcrecover* is an open source Bitcoin wallet password and seed recovery tool. It is designed for the case where you already know most of your password or seed, but need assistance in trying different possible combinations.

## Setup and Usage Tutorials ##
[I have created a growing playlist](https://www.youtube.com/playlist?list=PL7rfJxwogDzmd1IanPrmlTg3ewAIq-BZJ) that covers a number of usage examples for using this tool to recover seed phrases, BIP39 passphrases, etc.

My suggestion is that you find a scenario that is most-like your situation and try to replicate my examples to ensure that you have the tool set up and running correctly. If you have a specific situation that isn't covered in these tutorials, let me know and I can look into creating a video for that.

If this tool or other content on my YouTube channel was helpful, feel free to send a tip to:

BTC: 37hiiSB1Poj6Shs8WawPS2HjT2jzHkFSQi

BCH: qr9qenlgjh0xlyz802h70ul69rpdj8z6qyuh7m79ah

LTC: MRWnUcsyofisVp5GvX7nxMog5caneycKZ6

ETH: 0x14b2E26021d0Ce8E2cE6a2Eb6E2690714bB18E17

VTC: vtc1qxauv20r2ux2vttrjmm9eylshl508q04uju936n

ZEN: znUihTHfwm5UJS1ywo911mdNEzd9WY9vBP7


## Quick Start ##

To try recovering your password, please start with the **[Password Recovery Quick Start](TUTORIAL.md#btcrecover-tutorial)**.

If you mostly know your recovery seed/mnemonic (12-24 recovery words), but think there may be a mistake in it, please see the **[Seed Recovery Quick Start](docs/Seedrecover_Quick_Start_Guide.md)**.

## Thanks to Gurnec ##

This tool builds on the original work of Gurnec.

If you find *btcrecover* helpful, please consider a small donation to them too:
**[3Au8ZodNHPei7MQiSVAWb7NB2yqsb48GW4](bitcoin:3Au8ZodNHPei7MQiSVAWb7NB2yqsb48GW4?label=btcrecover)**

**Thank You!**


## Features ##

 * Bitcoin wallet password recovery support for:
     * [Armory](https://btcarmory.com/)
     * [Bitcoin Unlimited](https://www.bitcoinunlimited.info/)/[Classic](https://bitcoinclassic.com/)/[XT](https://bitcoinxt.software/)/[Core](https://bitcoincore.org/)
     * [MultiBit HD](https://multibit.org/) and [MultiBit Classic](https://multibit.org/help/v0.5/help_contents.html)
     * [Electrum](https://electrum.org/) (1.x and 2.x)
     * Most wallets based on [bitcoinj](https://bitcoinj.github.io/), including [Hive for OS X](https://github.com/hivewallet/hive-mac/wiki/FAQ)
     * BIP-39 passphrases, Bitcoin & Ethereum supported (e.g. [TREZOR](https://www.bitcointrezor.com/) & [Ledger](https://www.ledgerwallet.com/) passphrases)
     * [mSIGNA (CoinVault)](https://ciphrex.com/products/)
     * [Blockchain.info](https://blockchain.info/wallet)
     * [pywallet --dumpwallet](https://github.com/jackjack-jj/pywallet) of Bitcoin Unlimited/Classic/XT/Core wallets
     * [Bitcoin Wallet for Android/BlackBerry](https://play.google.com/store/apps/details?id=de.schildbach.wallet) spending PINs and encrypted backups
     * [KnC Wallet for Android](https://github.com/kncgroup/bitcoin-wallet) encrypted backups
     * [Bither](https://bither.net/)
 * Altcoin password support for most wallets derived from one of those above, including:
     * [Litecoin Core](https://litecoin.org/)
     * [Electrum-LTC](https://electrum-ltc.org/)
     * [Litecoin Wallet for Android](https://litecoin.org/) encrypted backups
     * [Dogecoin Core](http://dogecoin.com/)
     * [MultiDoge](http://multidoge.org/)
     * [Dogecoin Wallet for Android](http://dogecoin.com/) encrypted backups
 * Bitcoin & Ethereum seed recovery support for:
     * [Electrum](https://electrum.org/) (1.x and 2.x, plus wallet file loading support)
     * BIP-32/39 compliant wallets ([bitcoinj](https://bitcoinj.github.io/)), including:
         * [MultiBit HD](https://multibit.org/)
         * [Bitcoin Wallet for Android/BlackBerry](https://play.google.com/store/apps/details?id=de.schildbach.wallet) (with seeds previously extracted by [decrypt\_bitcoinj\_seeds](https://github.com/gurnec/decrypt_bitcoinj_seed))
         * [Hive for Android](https://play.google.com/store/apps/details?id=com.hivewallet.hive.cordova), [for iOS](https://github.com/hivewallet/hive-ios), and [Hive Web](https://hivewallet.com/)
         * [breadwallet for iOS](https://breadwallet.com/)
     * BIP-32/39/44 Bitcoin & Ethereum compliant wallets, including:
         * [Mycelium for Android](https://wallet.mycelium.com/)
         * [TREZOR](https://www.bitcointrezor.com/)
         * [Ledger](https://www.ledgerwallet.com/)
         * [Jaxx](https://jaxx.io/)
         * [MyEtherWallet](https://www.myetherwallet.com/)
         * [Bither](https://bither.net/)
         * [Blockchain.info](https://blockchain.info/wallet)
 * [Free and Open Source](http://en.wikipedia.org/wiki/Free_and_open-source_software) - anyone can download, inspect, use, and redistribute this software
 * Supported on Windows, Linux, and OS X
 * Support for Unicode passwords and seeds
 * Multithreaded searches, with user-selectable thread count
 * Experimental [GPU acceleration](docs/GPU_Acceleration.md) for Bitcoin Unlimited/Classic/XT/Core, Armory, and derived altcoin wallets
 * Wildcard expansion for passwords
 * Typo simulation for passwords and seeds
 * Progress bar and ETA display (at the command line)
 * Optional autosave - interrupt and continue password recoveries without losing progress
 * Automated seed recovery with a simple graphical user interface
 * “Offline” mode for nearly all supported wallets - use one of the [extract scripts (click for more information)](docs/Extract_Scripts.md) to extract just enough information to attempt password recovery, without giving *btcrecover* or whoever runs it access to *any* of the addresses or private keys in your Bitcoin wallet.
 * “Nearly offline” mode for Armory - use an [extract script (click for more information)](docs/Extract_Scripts.md) to extract a single private key for attempting password recovery. *btcrecover* and whoever runs it will only have access to this one address/private key from your Bitcoin wallet (read the link above for an important caveat).

# Basic Password/Passphrase Recoveries

None of these examples are concerned with arguments that you would use for different types of typos, tokenlists, etc.

The idea is that, if you are running this tool on Windows, you can directly copy/paste any of these examples. (They all use the same seeds and addresses that are in the automatic tests)

They will all find a result almost straight away.

**Basic Passwordlist used in basic examples below**
``` linenums="1"
{% include "common_passwordlist.txt" %}
```

## BIP38 Encrypted Paper Wallet Recovery.
**Notes**
BIP38 wallets are encrypted via sCrypt, so will be very slow to brute-force. GPU acceleration for these wallets is available, but doesn't offer much of a performance boost unless you have multiple GPUs or a particularly powerful GPU relative to your CPU... (Or some kind of dedicated OpenCL accelerator)

**Supported wallets**

* [bitaddress.org](https://www.bitaddress.org/)
* [liteaddress.org](https://liteaddress.org/)
* [paper.dash.org](https://paper.dash.org/)

And just about any other BIP38 encrypted private keys.

**Commands**

For Bitcoin (No coin needs to be specified, Bitcoin is checked by default)
```
python btcrecover.py --bip38-enc-privkey 6PnM7h9sBC9EMZxLVsKzpafvBN8zjKp8MZj6h9mfvYEQRMkKBTPTyWZHHx --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>
For Litecoin
```
python btcrecover.py --bip38-enc-privkey 6PfVHSTbgRNDaSwddBNgx2vMhMuNdiwRWjFgMGcJPb6J2pCG32SuL3vo6q --bip38-currency litecoin --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>
For Dash
```
python btcrecover.py --bip38-enc-privkey 6PnZC9Snn1DHyvfEq9UKUmZwonqpfaWav6vRiSVNXXLUEDAuikZTxBUTEA --bip38-currency dash --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>
## Brainwallets
**Notes**
Brainwallets are a very old (**and very unsafe**) type of wallet. Given this, most of them still produce addresses based on "uncompressed"

**Supported wallets**

* Sha256(Passphrase) Wallets
    * [bitaddress.org](https://www.bitaddress.org/)
    * [segwitaddress.org](https://segwitaddress.org/)
    * [liteaddress.org](https://liteaddress.org/)
    * [paper.dash.org](https://paper.dash.org/)
* Warpwallet Wallets
    * [WarpWallet](https://keybase.io/warp/)
    * [Memwallet](https://dvdbng.github.io/memwallet/)
    * [Mindwallet](https://patcito.github.io/mindwallet/)
  
### Sha256(Passphrase) Wallets
**Commands**

Basic Bitcoin Command (Will check both compressed and uncompressed address types, even though in this example this is a compressed address)
```
python btcrecover.py --brainwallet --addresses 1BBRWFHjFhEQc1iS6WTQCtPu2GtZvrRcwy --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>

Bitcoin Wallet, but set to only check uncompressed addresses. (Only use this for VERY old wallets that you are sure aren't a compressed address, though also consider that uncompressed is the default... Only gives a small speed boost)

```
python btcrecover.py --brainwallet --addresses 1MHoPPuGJyunUB5LZQF5dXTrLboEdxTmUm --skip-compressed --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>

P2SH Bitcoin Wallet (Like the kind you would get of something like segwitaddress.org, as of 2021, these are all compressed type addresses, so can skip checking uncomrpessed ones...)
```
python btcrecover.py --brainwallet --addresses 3C4dEdngg4wnmwDYSwiDLCweYawMGg8dVN --skip-uncompressed --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>

Bech32 Bitcoin Wallet. (From segwitaddress.org)
```
python btcrecover.py --brainwallet --addresses bc1qth4w90jmh0a6ug6pwsuyuk045fmtwzreg03gvj --skip-uncompressed --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>

Litecoin Wallet (From liteaddress.org - These are all uncompressed with no option to use compressed) No extra arguments are needed for these types of wallets.
```
python btcrecover.py --brainwallet --addresses LfWkecD6Pe9qiymVjYENuYXcYpAWjU3mXw --skip-compressed --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>

Dash Wallet (From paper.dash.org) - No compression parameters specificed, so it will just check both
```
python btcrecover.py --brainwallet --addresses XvyeDeZAGh8Nd7fvRHZJV49eAwNvfCubvB --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>


Dash Wallet (From paper.dash.org - Or if you know you used a compressed one... (Though Uncompressed is the default)
```
python btcrecover.py --brainwallet --addresses XksGLVwdDQSzkxK1xPmd4R5grcUFyB3ouY --skip-uncompressed --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>

### Warpwallets
Note: At this time, only Bitcoin and Litecoin are supported... (Eth could be easily added)

**Commands**

Basic Bitcoin Wallet with "btcr-test-password" as the salt. (Warpwallet suggested using your email address) These wallets are all "uncompressed" type, but the performance gain for this is so small compared to how long the sCrypt operation takes, it isn't worth not checking both types...
```
python btcrecover.py --warpwallet --warpwallet-salt btcr-test-password --addresses 1FThrDFjhSf8s1Aw2ed5U2sTrMz7HicZun --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
<br>
Basic Litecoin Wallet with "btcr-test-password" as the salt. (Like what memwallet or mindwallet produces, so you need to add the --crypto argment and specify litecoin) These wallets are all "uncompressed" type, but the performance gain for this is so small compared to how long the sCrypt operation takes, it isn't worth not checking both types...

```
python btcrecover.py --warpwallet --warpwallet-salt btcr-test-password --crypto litecoin --addresses LeBzGzZFxRUzzRAtm8EB2Dw74jRfQqUZeq --passwordlist ./docs/Usage_Examples/common_passwordlist.txt
```
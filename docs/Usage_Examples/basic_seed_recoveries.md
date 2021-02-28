# Basic Password/Passphrase Recoveries

The idea is that, if you are running this tool on Windows, you can directly copy/paste any of these examples. (They all use the same seeds and addresses that are in the automatic tests)

They will all find a result almost straight away.

## Seed Based Recovery Notes
**Notes**
Seedrecover.py has been set up so that the defaults should get a result for the majorty of simple "invalid menmonic" or "invalid seed" type errors. (Eg: Where you have an intact seed backup that has a typo in it)

It will search all account types for the supported cryptocurrencies, on all common derivation paths.

It will automatically run through four search phases that should take a few hours at most.
1. Single typo
2. Two typos, including one where you might have a completely different BIP39 word
3. Three typos, including one where you might have a completely different BIP39 word
4. Two typos that could be completely different words.

**Fully Supported wallets** (For supported cryptocurrencies)

* Hardware Wallets
    * Ledger Nano X and S
    * Trezor One and T
    * Keepkey
    * Safepal
    * Coldcard
    * Bitbox02
    * Cobo Vault
* Software Wallets
    * Electrum - Both V1 and V2 Seeds (This includes forks like Electrum-LTC, Electron-Cash, etc)
    * Coinomi
    * Wasabi
    * Edge Wallet
    * Mycelium
    * Exodus

**Wallets with Compatibility Issues**(Due to not following derivation standards...)

* Atomic Wallet. (Non-Standard and Unknown derivation ETH (And all ERC20 tokens), XRP)
* Abra Wallet. (Non-Standard seed format, first word is Non-BIP39 "at", the last 12 are BIP39 (and checksum) but unable to reproduce derivation)

## Examples
### Basic Bitoin Recoveries
**Note:** Most of the time you can just run seedrecover.py, even simply double click it and follow the graphical interface.

With a Native Segwit Address - One missing word, address generation limit of 5. (So address needs to be in the first 5 addresses in that account)
```
python seedrecover.py --wallet-type bip39 --addrs bc1qv87qf7prhjf2ld8vgm7l0mj59jggm6ae5jdkx2 --mnemonic "element entire sniff tired miracle solve shadow scatter hello never tank side sight isolate sister uniform advice pen praise soap lizard festival connect" --addr-limit 5
```

With a P2SH Segwit Address - One missing word, address generation limit of 5. (So address needs to be in the first 5 addresses in that account)
```
python seedrecover.py --wallet-type bip39 --addrs 3NiRFNztVLMZF21gx6eE1nL3Q57GMGuunG --mnemonic "element entire sniff tired miracle solve shadow scatter hello never tank side sight isolate sister uniform advice pen praise soap lizard festival connect" --addr-limit 5
```

# Multi-GPU Password Recovery using Vast.ai
YouTube Video can be found here: TBC

## Background
Vast.ai is a service where users around the world can rent out their spare GPU power. It is often cheaper and faster than using rented services from commercial providers like Google or Amazon... This service is mostly used for training AIs but is also useful for running OpenCL processes like BTCRecover and Hashcat. 

This is great in that if you don't have a powerful GPU, it makes it possible to cheaply attempt password recovery in a matter of hours that might take weeks if run on your own hardware, particularly if you only have a CPU and not a powerful GPU... (Or are otherwise unable to run a process like this that might take several days) It is particularly useful with BTCRecover when run using a wallet extract, in that this allows you to securely recover the password without the possibility that the rented server owner can steal your funds.

**This process is not secure for seed recovery, BIP39 seed recovery or where you upload the wallet file to the cloud server...**

## Performance

Blockchain.com Bechmark

`python3 btcrecover.py --wallet ./btcrecover/test/test-wallets/blockchain-v3.0-MAY2020-wallet.aes.json --performance --enable-opencl`

Bitcoin Core Benchmark

`python3 btcrecover.py --wallet ./btcrecover/test/test-wallets/bitcoincore-wallet.dat --performance --enable-gpu --global-ws 4096 --local-ws 256`

For the sake of comparison, I have run this benchmark on the following configurations.

| GPU(s) | Blockchain.com Performance (OpenCL) (kP/s) | Bitcoin Core (JTR) (kP/s) | Lowest Price ($/h) |
|---|---|---|---|
| i7 8750H (Reference-Local CPU) | 1 | 0.07 | 
| 1660ti (Reference-Local GPU) | 10 | 6.75 |
| 2x 1070 | 12.5 | 6.45 | 0.296 | 
| 1070ti | 6 | 3.2 | 0.127 |
| 10x 1080 | 46 | 13.5 | 1.64 | 
| 1080ti | 6 | 3.5 | 0.1 | 0.1 |
| 2x 1080ti | 10.1 | 6.1 | 0.3 |
| 6x 1080ti | 28 | 9.75 | 1.02 |
| 2x 2070 | 16.6 | 12 | 0.48 |
| 10x 2070 Super | 63 | 16 | 1.6 |
| 2080ti | 9.4 | 6.4 | 0.2 | 0.2 |
| 2x 2080ti | 19.5 | 10.8 | 0.4 |

_It's worth looking at the price/hour for different machines based on your time preference... Often a 2x 2080 machine will cost twice as much, to rent, but only require half as much rental time... Just be aware that the JTR kernel doesn't scale as well once you get past 2x GPUs_

## Vast.ai Instance Settings

**OS Image**

`nvidia/opencl:runtime-ubuntu18.04`

_(Hashcat images like dizcza/docker-hashcat:latest generally work too)_

**On-start script**
```
apt update
apt install python3 python3-pip nano mc git -y
git clone https://github.com/3rdIteration/btcrecover.git
pip3 install pyopencl==2019.1.1
pip3 install -r ~/btcrecover/requirements.txt
update-locale LANG=C.UTF-8
echo "set -g terminal-overrides \"xterm*:kLFT5=\eOD:kRIT5=\eOC:kUP5=\eOA:kDN5=\eOB:smkx@:rmkx@\"" > ~/.tmux.conf
```

_This will download all updates, clone BTCRecover in to the home folder, install all dependancies and get the environment ready to use BTCRecover. It normally finishes running within a few minutes of the vast.ai host reaching the "Successfully Loaded" status..._

**Disk Space to Allocate**

1GB is fine unless you are trying to use an AddressDB file... (In which case you will need to allocate sufficient space for the uncompressed AddressDB file + 1GB)

## What you will need
* Secure Shell (SSH) software client like Putty (on Windows)
* A Secure File Transfer tools like WinSCP (on Windows)
* A Credit Card (To pay for Vast.ai time)

## Step-By Step Process
1) Create a wallet extract for your wallet. (Optionally: Start the process on your PC through to the password counting step, then copy the autosave file to the Vast.ai host)
2) Create an account on https://vast.ai/
3) Select a server, add the server settings above and create it
4) Connect to the server via SCP and copy required files (Possibly including autosave files)
5) Connect and check that everything works... (Running one of the benchmark commands above is a good bet)
6) Run your BTCRecover command.
7) Destroy the server once complete.

**Make sure that you allocate at least one thread per GPU...**

## Common Issues
Requirements not correctly installed...

**Connection Refused**
Double check the connection IP and port, if you still can't connect, click "destroy" and try a different host... 

**OpenCL Program Build Failed**
The error that it exits on will be: `TypeError: 'int' object is not subscriptable`

But if you scroll up, you will see:
```
`clBuildProgram failed: BUILD_PROGRAM_FAILURE - clBuildProgram failed: BUILD_PROGRAM_FAILURE - clBuildProgram failed: BUILD_PROGRAM_FAILURE

Build on <pyopencl.Device 'GeForce GTX 1070 Ti' on 'NVIDIA CUDA' at 0x2e40da0>:

===========================================================================
Build on <pyopencl.Device 'GeForce GTX 1070 Ti' on 'NVIDIA CUDA' at 0x2e40df0>:


(options: -I /usr/local/lib/python3.6/dist-packages/pyopencl/cl)
(source saved as /tmp/tmpqqq0xe7b.cl)`
```

Alternatively you might see: `UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 31: ordinal not in range(128)` if trying to run the JTR kernel...

_This is an issue on this particular vast.ai host you have rented, destroy it and try a different one..._

**No BTCRecover folder...**

type
`cat onstart.log`
to see how the on-start script is going... It might be stuck, may have hit an error, but simply giving it some more time may help...

In this situation, you can either manually run the start commands one at a time, but if they have failed, there are probably other issues with the host... If in doubt, just destroy the server and rent a different one... 

**Anything else...**
Destroy the vast.ai host you have rented and rent another one... It's possible to get two faulty servers in a row, so try a new server at least 3 times...

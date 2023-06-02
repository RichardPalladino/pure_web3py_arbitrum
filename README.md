# Pure Web3.py Arbitrum
### Exploration of local Arbitrum node capabilities with Web3.py

Until recently, I have only used remote nodes.  I have recently spun up a node to try out local node performance.

While I often use Brownie, its development has stagnated and Ape just isn't up to speed yet (at least not for my tastes).

I've been pivoting back to pure web3.py lately, and I may even breakout the Hardhat again....

###  Plan / To-do:

* Re-write a Uniswap V2-compatible pool scraping script that I have written to instead use web sockets and inter-process communication so I can test performance of all 3 types (http, ws, ipc) with my local node daemon/container..
* Play with the performance of each of these basic provider types using different multi-threaded and/or concurrency methods to see if any one in particular works best.
* Test the scripts with Python v3.11, PyPy, and Pyston (both full and lite versions) to see if there are any compatability issues with web3.py or my async/multi-threaded tests.
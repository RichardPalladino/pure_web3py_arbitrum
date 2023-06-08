# Pure Web3.py Arbitrum
### Exploration of local Arbitrum node capabilities with Web3.py

Until recently, I have only used remote nodes.  I have recently spun up a node to try out local node performance.

While I often use Brownie, its development has stagnated and Ape just isn't up to speed yet (at least not for my tastes).

I've been pivoting back to pure web3.py lately, and I may even breakout the Hardhat again....

###  Plan / To-do:

* Re-write a Uniswap V2-compatible pool scraping script that I have written to instead use web sockets and inter-process communication so I can test performance of all 3 types (http, ws, ipc) with my local node daemon/container..
* Play with the performance of each of these basic provider types using different multi-threaded and/or concurrency methods to see if any one in particular works best.
* Test the scripts with Python v3.11, PyPy, and Pyston (both full and lite versions) to see if there are any compatability issues with web3.py or my async/multi-threaded tests.

### Average runtime in my environment:

* Vanilla / template version:                   7.78 minutes
* get_v2pools_asyncHttp:                        7.30 minutes
* get_v2pools_asyncHttp-ws:                     6.07 minutes
* get_v2pools_asyncHttp-ipc:                    5.81 minutes
* get_v2pools_threadPool:                       5.72 minutes
* get_v2pools_threadPool-IPC:                   6.26 minutes <--- worse than IPC with partial threadpoolexecutor
* get_v2pools_multithreaded-IPC (6 workers):    6.78 minutes <--- EVEN WORSE (got worse as I added more workers - 8.47 mins with 12 workers)
* get_v2pools_extended-threadPool :             12.63 minutes


### Other findings:

* It does not appear that multiprocessing works with Web3.py, so I was not able to achieve true parallelism with my basic tests.
* There is a sweet-spot where concurrency helps with certain IO operations and is not over-applied.
* Threadpools and asyncio both have overhead, so use should be deliberate and not liberal.
* IPC is always fastest.

### PyPy:

Install on Ubuntu with:

`sudo add-apt-repository ppa:pypy/ppa
sudo apt update
sudo apt install pypy3`


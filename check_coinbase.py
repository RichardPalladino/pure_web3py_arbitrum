import asyncio
from web3 import Web3, AsyncWeb3, AsyncHTTPProvider
from web3.eth import AsyncEth


async def main():
    w3 = AsyncWeb3(
        AsyncWeb3.AsyncHTTPProvider("http://127.0.0.1:8545"),
        modules={"eth": (AsyncEth,)},
        middlewares=[],
    )
    coinbase = await w3.eth.coinbase
    print(coinbase)


if __name__ == "__main__":
    asyncio.run(main())

from time import perf_counter
from math import round
import asyncio
import json
import os

# import requests
from dotenv import load_dotenv
from web3 import Web3, AsyncWeb3, AsyncHTTPProvider

load_dotenv("./.env")

# W3_HTTP_PROVIDER = os.getenv("CHAINSTACK_ARBITRUM")
# W3_WSS_PROVIDER = os.getenv("CHAINSTACK_ARBITRUM_WSS")

W3_HTTP_PROVIDER = "http://127.0.0.1:8547"
W3_WSS_PROVIDER = "ws://127.0.0.1:8548"

IPC_PATH = (
    "/home/user/.arbitrum/data/ipc/path"  # must have permission to access, read/write
)

LP_ABI = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
ERC20_ABI = '[{"constant":false,"inputs":[{"name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newImplementation","type":"address"},{"name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"implementation","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"admin","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_implementation","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":false,"name":"previousAdmin","type":"address"},{"indexed":false,"name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"implementation","type":"address"}],"name":"Upgraded","type":"event"}]'


FACTORY_ABI = []
FACTORY_ABI[
    0
] = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"migrator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pairCodeHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_migrator","type":"address"}],"name":"setMigrator","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
FACTORY_ABI[
    1
] = '[{"inputs":[{"internalType":"address","name":"feeTo_","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prevOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"FeePercentOwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prevFeeTo","type":"address"},{"indexed":true,"internalType":"address","name":"newFeeTo","type":"address"}],"name":"FeeToTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"prevOwnerFeeShare","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ownerFeeShare","type":"uint256"}],"name":"OwnerFeeShareUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prevOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"length","type":"uint256"}],"name":"PairCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"referrer","type":"address"},{"indexed":false,"internalType":"uint256","name":"prevReferrerFeeShare","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"referrerFeeShare","type":"uint256"}],"name":"ReferrerFeeShareUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prevOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"SetStableOwnershipTransferred","type":"event"},{"constant":true,"inputs":[],"name":"OWNER_FEE_SHARE_MAX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"REFERER_FEE_SHARE_MAX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeInfo","outputs":[{"internalType":"uint256","name":"_ownerFeeShare","type":"uint256"},{"internalType":"address","name":"_feeTo","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feePercentOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"ownerFeeShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"referrersFeeShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feePercentOwner","type":"address"}],"name":"setFeePercentOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"setOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"newOwnerFeeShare","type":"uint256"}],"name":"setOwnerFeeShare","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"referrer","type":"address"},{"internalType":"uint256","name":"referrerFeeShare","type":"uint256"}],"name":"setReferrerFeeShare","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_setStableOwner","type":"address"}],"name":"setSetStableOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"setStableOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'
FACTORY_ABI[
    2
] = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
FACTORY_ABI[
    3
] = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"bool","name":"stable","type":"bool"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"inputs":[],"name":"MAX_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"acceptFeeManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"acceptPauser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"feeManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"_stable","type":"bool"}],"name":"getFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"bool","name":"","type":"bool"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_proxyAdmin","type":"address"},{"internalType":"address","name":"_pairImplementation","type":"address"},{"internalType":"address","name":"_voter","type":"address"},{"internalType":"address","name":"msig","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isPair","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isPaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pairCodeHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"pairFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pairImplementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pauser","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingFeeManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingPauser","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxyAdmin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"_stable","type":"bool"},{"internalType":"uint256","name":"_fee","type":"uint256"}],"name":"setFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_feeManager","type":"address"}],"name":"setFeeManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_implementation","type":"address"}],"name":"setImplementation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_pair","type":"address"},{"internalType":"uint256","name":"_fee","type":"uint256"}],"name":"setPairFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_state","type":"bool"}],"name":"setPause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_pauser","type":"address"}],"name":"setPauser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stableFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"volatileFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"voter","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'


bogus_addresses = []
# solidly_forks = {}  # factory -> isStable, stableSwap bools


def serialize_sets(obj):  # so JSON can handle sets
    if isinstance(obj, set):
        return list(obj)

    return obj


def get_async_web3_provider():
    return AsyncWeb3(AsyncHTTPProvider(W3_HTTP_PROVIDER))


def get_web3_provider():
    return Web3(Web3.HTTPProvider(W3_HTTP_PROVIDER))


def get_wss_provider():
    return Web3(Web3.WebsocketProvider(W3_WSS_PROVIDER))


def get_ipc_provider():
    return Web3(Web3.IPCProvider(IPC_PATH))


def get_deployed_factory(w3) -> dict:
    global bogus_addresses
    factories = {}

    # load factory dict
    with open("dexs.json", "r") as dex_file:
        fact_dict = json.load(dex_file)

    for dex, values in fact_dict:
        print(f"{dex} has {str(values)} values")
        try:
            factory = w3.eth.contract(
                address=values["factory"], abi=LP_ABI[values["fee_type"]]
            )

            factories[values["factory"]] = {
                "length": factory.allPairsLength(),
                "fee_type": values["fee_type"],
            }
            if values["fee_type"] == 0:
                factories[values["factory"]]["max_fee"] = values["max_fee"]
            if values["solidly"]:
                if values["stableSwap"]:
                    factories[values["factory"]]["stable_swap"] = 2
                else:
                    factories[values["factory"]]["stable_swap"] = 1
            else:
                factories[values["factory"]]["stable_swap"] = 0
        except Exception as err:
            print(
                f'Function "get_num_deployed" failed on {active_network} network {dex} factory, with the following error:\n{err}'
            )
            bogus_addresses.append(
                {
                    "factory": str(values["factory"]),
                    "reason": f'interface.IUniswapV2Factory failure on {str(active_network)} with {values["factory"]} factory and error "{err}"',
                }
            )

    return factories


def get_pool_data(_address, _factory_data, w3_provider) -> dict:
    result = None
    try:
        pool = w3_provider.eth.contract(address=_address, abi=LP_ABI)
        tmp_token0_address = pool.token0()
        tmp_token1_address = pool.token1()
        if _factory_data["stable_swap"] == 2:
            if pool.stableSwap():
                stable_pool = True
                print(f"{_address} is Solidly stable LP")
            else:
                stable_pool = False
        elif _factory_data["stable_swap"] == 1:
            if pool.stable():
                stable_pool = True
                print(f"{_address} is Solidly stable LP")
            else:
                stable_pool = False
        # do I need to do anything if stable_swap == 0 ?
        else:
            stable_pool = False

        if _factory_data["fee_type"] == 0:
            fee = _factory_data["max_fee"]
        elif _factory_data["fee_type"] == 1:
            fee = round((pool.swapFee() / 10000), 4)

        result = {
            "lp_address": _address,
            "tokens": [tmp_token0_address, tmp_token1_address],
            "reserves": pool.getReserves(),
            "stable_pool": stable_pool,
            "fee": fee,
        }
        if stable_pool:
            result["stable_type"] = _factory_data["stable_swap"]

    except Exception as err:
        print(
            f'Received the following error when querying blockchain using "get_pool_data()" for {_address}:\n  {err}'
        )
        bogus_addresses.append(
            {
                "lp_address": str(_address),
                "reason": f'error at "get_pool_data()": {err}',
            }
        )
        result = False
    finally:
        return result


def get_erc20_data(_address, _w3) -> dict:
    result = None
    try:
        tmp_token = w3.eth.contract(address=_address, abi=ERC20_ABI)
        result = {
            "symbol": tmp_token.symbol(),
            "name": tmp_token.name(),
            "decimals": tmp_token.decimals(),
        }
    except Exception as err:
        print(
            f'Received the following error when querying blockchain using "get_erc20_data()" for {_address}:\n  {err}'
        )
        bogus_addresses.append(
            {
                "erc20_address": str(_address),
                "reason": f'error at "get_erc20_data()": {err}',
            }
        )
        result = False
    finally:
        return result


def main() -> None:
    global bogus_addresses

    start_time = perf_counter()
    factory_lps = {}
    pairs = {}
    erc_20s = {}

    w3 = get_web3_provider

    # get a dictionary of all factories, and their attributes factory_address -> values
    factories = get_deployed_factory(w3)

    print(factories)

    for factory_address, values in factories.items():
        try:
            factory = w3.eth.contract(address=factory_address, abi=values["fee_type"])
        except Exception as err:
            print(
                f'"IUniswapV2Factory" failed in {factory} factory, with the following error:\n{err}'
            )
            bogus_addresses.append(
                {
                    "factory": str(factory),
                    "reason": f"interface.IUniswapV2Factory error: {err}",
                }
            )
            continue
        factory_lps[factory_address] = []
        num_pools = factories[factory_address]["length"]
        # Loop through each LP listed in the Factory
        for i in range(0, num_pools):
            try:
                tmp_lp_address = factory.allPairs(i)
            except Exception as err:
                print(
                    f"Received the following error when querying {factory_address} allPairs() at index {i}:\n  {err}"
                )
                bogus_addresses.append(
                    {
                        "factory": str(factory_address),
                        "index": str(i),
                        "reason": f'Error querying "factory.allpairs()": {err}',
                    }
                )
                # if it's bogus, make it one of my addresses for comparison
                tmp_lp_address = Web3.to_checksum_address(
                    "0x4AfA03ED8ca5972404b6bDC16Bea62b77Cf9571b"
                )
                pairs["0x4AfA03ED8ca5972404b6bDC16Bea62b77Cf9571b"] = False
            ## Get dict of pool data, if tmp_lp_address isn't bogus, i.e., has been made one of my addresses
            if tmp_lp_address != Web3.to_checksum_address(
                "0x4AfA03ED8ca5972404b6bDC16Bea62b77Cf9571b"
            ):
                pairs[Web3.to_checksum_address(tmp_lp_address)] = get_pool_data(
                    Web3.to_checksum_address(tmp_lp_address),
                    factories[factory_address],
                    w3,
                )  # factories is a dict of factory_address -> factory values (num_pools, router, fee_type, solidly, etc.)
            #####
            # Check for errors with either LP, token0 or token1
            #####
            if (pairs[tmp_lp_address] is None) or (pairs[tmp_lp_address] == False):
                pairs[tmp_lp_address] = False
                print(f"LP {tmp_lp_address} is invalid")
                bogus_addresses.append(
                    {
                        "lp_address": str(tmp_lp_address),
                        "reason": f"either get_pool_data() failure or one of the tokens is bad",
                    }
                )
                continue
            else:
                pairs[tmp_lp_address]["factory_address"] = factory_address
                ## Add dicts of each token data
                # Token0
                token0_address = pairs[tmp_lp_address]["tokens"][0]
                # Reduce direct blockchain calls, check if we've already populated the token data
                if token0_address in erc_20s.keys():
                    # Make sure the pool has been found and does not return an error
                    if erc_20s[token0_address] != False:
                        pairs[tmp_lp_address]["token0"] = {
                            "address": token0_address,
                            **erc_20s[token0_address],
                        }
                    else:
                        # try again?
                        tmp_token = get_erc20_data(token0_address)
                        # If querying the blockchain returns None for the pool, there was an error
                        if (tmp_token is None) or (tmp_token == False):
                            erc_20s[token0_address] = False
                            pairs[tmp_lp_address] = False
                            print(
                                f"{tmp_lp_address} is invalid because {token0_address} was tracked as False and returned None again"
                            )
                            bogus_addresses.append(
                                {
                                    "invalid_erc20": str(token0_address),
                                    "lp_address": str(tmp_lp_address),
                                    "dex_factory": str(factory_address),
                                }
                            )
                            continue
                        else:
                            erc_20s[token0_address] = tmp_token
                            pairs[tmp_lp_address]["token0"] = {
                                "address": token0_address,
                                **tmp_token,
                            }

                else:
                    # If we haven't already populated the pool data, query the blockchain to get it
                    tmp_token = get_erc20_data(token0_address)
                    # If querying the blockchain returns None for the pool, there was an error
                    if (tmp_token is None) or (tmp_token == False):
                        erc_20s[token0_address] = False
                        pairs[tmp_lp_address] = False
                        print(
                            f"{tmp_lp_address} is invalid because {token0_address} returned none or False"
                        )
                        bogus_addresses.append(
                            {
                                "invalid_erc20": str(token0_address),
                                "lp_address": str(tmp_lp_address),
                                "dex_factory": str(factory_address),
                            }
                        )
                        continue
                    else:
                        erc_20s[token0_address] = tmp_token
                        pairs[tmp_lp_address]["token0"] = {
                            "address": token0_address,
                            **tmp_token,
                        }

                # Same for token1 as token0, above
                if pairs[tmp_lp_address] != False:
                    token1_address = pairs[tmp_lp_address]["tokens"][1]
                    if token1_address in erc_20s.keys():
                        if erc_20s[token1_address] != False:
                            pairs[tmp_lp_address]["token1"] = {
                                "address": token1_address,
                                **erc_20s[token1_address],
                            }
                        else:
                            # if the token is False, the entire pool is false, right?
                            # try again
                            tmp_token = get_erc20_data(token1_address)
                            if (tmp_token is None) or (tmp_token == False):
                                erc_20s[token1_address] = False
                                pairs[tmp_lp_address] = False
                                print(
                                    f"{tmp_lp_address} invalid because {token1_address} is tracked as False and returned None"
                                )
                                bogus_addresses.append(
                                    {
                                        "invalid_erc20": str(token1_address),
                                        "lp_address": str(tmp_lp_address),
                                        "dex_factory": str(factory_address),
                                    }
                                )

                                continue
                            else:
                                erc_20s[token1_address] = tmp_token
                                pairs[tmp_lp_address]["token1"] = {
                                    "address": token1_address,
                                    **tmp_token,
                                }

                    else:
                        tmp_token = get_erc20_data(token1_address)
                        if (tmp_token is None) or (tmp_token == False):
                            erc_20s[token1_address] = False
                            pairs[tmp_lp_address] = False
                            print(
                                f"{tmp_lp_address} is invalid because {token1_address} returned none or False"
                            )
                            bogus_addresses.append(
                                {
                                    "invalid_erc20": str(token1_address),
                                    "lp_address": str(tmp_lp_address),
                                    "dex_factory": str(factory_address),
                                }
                            )

                            continue
                        else:
                            erc_20s[token1_address] = tmp_token
                            pairs[tmp_lp_address]["token1"] = {
                                "address": token1_address,
                                **tmp_token,
                            }

                # If either tokens returns an error, set the LP dictionary to False
                if (
                    (erc_20s[token0_address] == False)
                    or (erc_20s[token0_address] == False)
                    or (pairs[tmp_lp_address] == False)
                ):
                    pairs[tmp_lp_address] = False
                    print(
                        f"One of the tokens in {tmp_lp_address} is invalid, LP is invalid"
                    )
                    continue
                elif ("token0" not in pairs[tmp_lp_address]) or (
                    "token1" not in pairs[tmp_lp_address]
                ):
                    pairs[tmp_lp_address] = False
                    print(f"Missing one of the tokens in {tmp_lp_address}")
                    continue
                else:
                    # if the liquidity is excessively low, set the LP dictionary to false
                    if (
                        pairs[tmp_lp_address]["reserves"][0]
                        / (10 ** pairs[tmp_lp_address]["token0"]["decimals"])
                    ) < 1 or (
                        pairs[tmp_lp_address]["reserves"][1]
                        / (10 ** pairs[tmp_lp_address]["token1"]["decimals"])
                    ) < 1:
                        print(f"{tmp_lp_address} has too little reserves")
                        bogus_addresses.append(
                            {
                                "lp_address": str(tmp_lp_address),
                                "reason": "low reserves",
                            }
                        )
                        pairs[tmp_lp_address] = False
                    else:
                        factory_lps[factory_address].append(tmp_lp_address)
        # Close-out processing of the DEX / factory set
        print(f"{factory_address} currently has {num_pools} liquidity pools")

    tmp_json = json.dumps(factory_lps, indent=3)
    with open("reports/lps_per_dex.json", "w") as f_out:
        f_out.write(tmp_json)

    # Output the current state of the pairs and LP list dictionaries
    tmp_json = json.dumps(pairs, indent=3)
    with open("reports/lp_dictionary.json", "w") as f_out:
        f_out.write(tmp_json)
    tmp_json = json.dumps(bogus_addresses, indent=3)
    with open("reports/invalid_addresses.json", "w") as f_out:
        f_out.write(tmp_json)

    end_time = perf_counter()
    total_time = (end_time - start_time) / 60
    print(f"This took {total_time} minutes.")


if __name__ == "__main__":
    main()

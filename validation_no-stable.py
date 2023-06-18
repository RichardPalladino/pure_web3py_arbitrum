# Merged some script content down below
from datetime import datetime, timedelta
from requests import Session
from time import perf_counter
import fnmatch

# import asyncio
# import requests
import json
import os
import re

from dotenv import load_dotenv

load_dotenv()

SKIP_LPS = [
    "0xcC5caa099AbE383ecb0d84EE37aaFB0c50Ae34EF",
    "0xb0F550F8B437ED614bb3105aB781C9428C40e8eb",
    "0xE1501d4144E01b209eDc13548D2E3B94086F0BB6",
    "0x82439E9471B724b595b4812ef5f5FEAc417B8131",
    "0xe013D8EAd448D9D3Cf23EaC40530C29ead8d0dF5",
    "0x6c8e8427DB3C7825a60d3EfedEC3Af7C472F99f4",
    "0x424c29063d9371A26a7952AB376eBfEf031607A1",
    "0x24c0b4008dF007bBB34601BdA29e0996706e1174",
    "0xCcB02338Aad77f90c04f4adDC53BEFCD1aE96f59",
    "0xD64256b44F75Aa9E558F9d236a6e77CB2ee2Fcd2",
    "0x74b5d263E0ac1Ee69C2cDB3223ce589036B6fdDC",
    "0x0FE8148E11ebE044D9766394AD1DF0fBD7AfFAce",
    "0x8dBcA34f12B3bfF0E73076804d8937606Db87D5E",
    "0xF804D77fC2385940df327fc847c1d9b81C7A6A19",
    "0x2A964a2eaE2718024f38f12Eb1572FcCc5E63880",
    "0x7038543B76ABeA9e7ED750a9efd150d657EADfe2",
    "0x13940C3961f9df78578A5E967ffEb41695f90119",
    "0x3F70e8eAa8c842350D401e4e5C9Cef11E4D64297",
    "0xB1A5d7D6cb83B62fA3129DB079570C34D034c19c",
    "0x13C51fC061295CdD7ab340759DB0E194c203E476",
    "0x4AfA03ED8ca5972404b6bDC16Bea62b77Cf9571b",
    "0x89c85841CCFBaFe9588150BBC7b911cE776FAB90",
    "0xe3e757BC5Af026ae80095CDaace0B51a61f5e639",
    "0xD46F8323E6E5540746E2df154cc1056907e89C7A",
]  # frax share LP has reverse reserves

SKIP_DEXS = []

ETH_CONTRACTS = [
    "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    "0x662d0f9Ff837A51cF89A1FE7E0882a906dAC08a3",
    "0x73700aeCfC4621E112304B6eDC5BA9e36D7743D3",
    "0x8abD3951C43E23728921DAb587d44C2F0761d0B5",
]
USD_CONTRACTS = [
    "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
    "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    "0xFEa7a6a0B346362BF88A9e4A88416B77a57D6c2A",
    "0x17FC002b466eEc40DaE837Fc4bE5c67993ddBd6F",
    "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
]

AMMOUNT_USD = 2000.0
AMMOUNT_ETH = 1.0

# Global data dictionaries that will later get written to file
usd_prices = {}  # ERC20 contract --> Dollar price
eth_prices = {}  # ERC20 contract --> ETH price

low_usd_lps = {}  # LP --> ERC20 that has low USD
low_eth_lps = {}  # LP --> ERC20 that has low ETH

# ERC20 --> [pools that it's in]  ---- so I can build out the triads easier / faster
erc20_pools = {}
# Coinmarketcap response set
cmc_responses = {}
# Total LPs (not false)
lp_list = []


def serialize_sets(obj):  # So JSON can handle sets
    if isinstance(obj, set):
        return list(obj)
    return obj


def get_coinmarketcap_session():
    coinmarketcap_api_key = os.getenv("COINMARKETCAP_KEY")
    print(f"CoinmarketCap API Key: {coinmarketcap_api_key}")
    request_headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": coinmarketcap_api_key,
    }

    session = Session()
    session.headers.update(request_headers)
    return session


def build_erc20_pools(_erc20, _lp):
    if _erc20 in erc20_pools:
        erc20_pools[_erc20].add(_lp)
    else:
        erc20_pools[_erc20] = {_lp}


def first_pass(_lp_dict) -> dict:
    # FIRST PASS:
    # 1. Loop through LP data and check if one token is a USD or ETH equivalent
    # 2. Make LPs false if they don't have enough money
    # 3. Set USD or ETH equivalent price in the prices dicts for the other tokens if sufficient liquidity
    # 4. If they don't have an ETH or USD price, query coinmarketcap for the price of one token and add to the prices list

    # get coinmarketcap session

    endpoint_url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    coinmarketcap = get_coinmarketcap_session()

    no_prices = {}
    symbols_string = ""

    for lp, lp_data in _lp_dict.items():
        if lp_data == False:
            # or (lp in SKIP_LPS)
            # or (lp_data["factory_address"] in SKIP_DEXS)
            continue
        elif lp_data["stable_pool"] == True:
            _lp_dict[lp] = False
            continue

        token0_address = lp_data["tokens"][0]
        token1_address = lp_data["tokens"][1]

        if (token0_address in usd_prices) or (token1_address in usd_prices):
            # if I grabbed the price on one of the tokens earlier in this loop, check liquidity with the price data
            # In other words, if the token price in USD is known, check the reserves in the USD equivalent (also, this means it's not a USD or ETH contract)
            if (token0_address in usd_prices) and (
                lp_data["reserves"][0] / (10 ** lp_data["token0"]["decimals"])
            ) < AMMOUNT_USD:
                _lp_dict[lp] = False
                low_usd_lps[lp] = token0_address

            elif (token1_address in usd_prices) and (
                lp_data["reserves"][1] / (10 ** lp_data["token1"]["decimals"])
            ) < AMMOUNT_USD:
                _lp_dict[lp] = False
                low_usd_lps[lp] = token1_address
            else:
                # the LP has sufficient liquidity so track the pools in erc20_pools
                build_erc20_pools(token0_address, lp)
                build_erc20_pools(token1_address, lp)
                lp_list.append({lp: [token0_address, token1_address]})
                continue

        elif (token0_address in eth_prices) or (token1_address in eth_prices):
            # again, check the token against ETH prices
            if (token0_address in eth_prices) and (
                lp_data["reserves"][0] / (10 ** lp_data["token0"]["decimals"])
            ) < AMMOUNT_ETH:
                _lp_dict[lp] = False
                low_usd_lps[lp] = token0_address
            elif (token1_address in eth_prices) and (
                lp_data["reserves"][1] / (10 ** lp_data["token1"]["decimals"])
            ) < AMMOUNT_ETH:
                _lp_dict[lp] = False
                low_usd_lps[lp] = token1_address
            else:
                # the LP has sufficient liquidity so track the pools in erc20_pools
                build_erc20_pools(token0_address, lp)
                build_erc20_pools(token1_address, lp)
                lp_list.append({lp: [token0_address, token1_address]})
                continue

        else:
            # If the LP contract is not void/false and neither token yet has a USD or ETH price,
            # Check if one token is a USD equvalent
            if token0_address in USD_CONTRACTS:
                # check token0 liquidity
                decimals = lp_data["token0"]["decimals"]
                liquidity = lp_data["reserves"][0]
                total = liquidity / (10**decimals)
                if total >= AMMOUNT_USD:
                    # I can set the token1 USD price, as long as token1 isn't an ETH equivalent
                    if token1_address not in ETH_CONTRACTS:
                        # If t0 has enough USD, we can let this pass but also use the LP to determine t1's price in dollars
                        t1_liquidity = lp_data["reserves"][1] / (
                            10 ** lp_data["token1"]["decimals"]
                        )
                        usd_price = t1_liquidity / total
                        usd_prices[token1_address] = usd_price
                    # the LP has sufficient liquidity so track the pools in erc20_pools
                    build_erc20_pools(token0_address, lp)
                    build_erc20_pools(token1_address, lp)
                    lp_list.append({lp: [token0_address, token1_address]})
                    continue
                else:
                    # if token0 is a USD equivalent but the total ammount is less than required, mark the LP as void
                    _lp_dict[lp] = False
                    low_usd_lps[lp] = token0_address
                    continue

            elif token1_address in USD_CONTRACTS:
                # check token1 liquidity
                decimals = lp_data["token1"]["decimals"]
                liquidity = lp_data["reserves"][1]
                total = liquidity / (10**decimals)
                if total >= AMMOUNT_USD:
                    if token0_address not in ETH_CONTRACTS:
                        # If t1 has enough USD, we can let this pass but also use the LP to determine t0's price in dollars
                        t0_liquidity = lp_data["reserves"][0] / (
                            10 ** lp_data["token0"]["decimals"]
                        )
                        usd_price = t0_liquidity / total
                        usd_prices[token0_address] = usd_price
                    # the LP has sufficient liquidity so track the pools in erc20_pools
                    build_erc20_pools(token0_address, lp)
                    build_erc20_pools(token1_address, lp)
                    lp_list.append({lp: [token0_address, token1_address]})
                    continue
                else:
                    _lp_dict[lp] = False
                    low_usd_lps[lp] = token1_address
                    continue
            #
            # Check if one token is an ETH equivalent
            elif token0_address in ETH_CONTRACTS:
                # check token0 liquidity
                decimals = lp_data["token0"]["decimals"]
                liquidity = lp_data["reserves"][0]
                total = liquidity / (10**decimals)
                if total >= AMMOUNT_ETH:
                    if token1_address not in USD_CONTRACTS:
                        # If t0 has enough ETH, we can let this pass but also use the LP to determine t1's price in Ethereum
                        t1_liquidity = lp_data["reserves"][1] / (
                            10 ** lp_data["token1"]["decimals"]
                        )
                        eth_price = t1_liquidity / total
                        eth_prices[token1_address] = eth_price
                    # the LP has sufficient liquidity so track the pools in erc20_pools
                    build_erc20_pools(token0_address, lp)
                    build_erc20_pools(token1_address, lp)
                    lp_list.append({lp: [token0_address, token1_address]})
                    continue

                else:
                    _lp_dict[lp] = False
                    low_eth_lps[lp] = token0_address

            elif token1_address in ETH_CONTRACTS:
                # check token1 liquidity
                decimals = lp_data["token1"]["decimals"]
                liquidity = lp_data["reserves"][1]
                total = liquidity / (10**decimals)
                if total >= AMMOUNT_ETH:
                    if token0_address not in USD_CONTRACTS:
                        # If t1 has enough ETH, we can let this pass but also use the LP to determine t0's price in Ethereum
                        t0_liquidity = lp_data["reserves"][0] / (
                            10 ** lp_data["token0"]["decimals"]
                        )
                        eth_price = t0_liquidity / total
                        eth_prices[token0_address] = eth_price
                    # the LP has sufficient liquidity so track the pools in erc20_pools
                    build_erc20_pools(token0_address, lp)
                    build_erc20_pools(token1_address, lp)
                    lp_list.append({lp: [token0_address, token1_address]})

                else:
                    _lp_dict[lp] = False
                    low_eth_lps[lp] = token1_address

            ##  QUERY CoinmarketCap for prices, otherwise
            else:  # make a list of tokens that are in LPs without any ETH or USD equivalent token
                #  97 + 2 tokens = 99 and the limit is 100 -- this should do 98 at a time -- querying CoinmarketCap
                if len(no_prices) < 98:
                    if re.match(r"[a-zA-Z0-9]{2,12}$", lp_data["token0"]["symbol"]):
                        if token0_address not in no_prices:
                            no_prices[token0_address] = lp_data["token0"][
                                "symbol"
                            ].upper()
                            if symbols_string == "":
                                symbols_string = f"{no_prices[token0_address]}"
                            else:
                                symbols_string = (
                                    f"{symbols_string},{no_prices[token0_address]}"
                                )
                    if re.match(r"[a-zA-Z0-9]{2,12}$", lp_data["token1"]["symbol"]):
                        if token1_address not in no_prices:
                            no_prices[token1_address] = lp_data["token1"][
                                "symbol"
                            ].upper()
                            if symbols_string == "":
                                symbols_string = f"{no_prices[token1_address]}"
                            else:
                                symbols_string = (
                                    f"{symbols_string},{no_prices[token1_address]}"
                                )
                else:
                    response = coinmarketcap.get(
                        endpoint_url + f"?symbol={symbols_string}"
                    )
                    print(f"{symbols_string} response code {response.status_code}")
                    if response.status_code == 200:
                        response = json.loads(response.text)
                        response = response["data"]
                        for erc20, symbol in no_prices.items():
                            if response[symbol] != []:
                                # get price from the response for the symbol
                                usd_price = response[symbol][0]["quote"]["USD"]["price"]
                                # get last updated from the response for the symbol
                                date_str = response[symbol][0]["last_updated"]
                                last_updated = datetime.fromisoformat(
                                    date_str.replace("Z", "+00:00")
                                )
                                # only accept the price if it's less than 24 hours old
                                tmp_now = datetime.utcnow()
                                if (
                                    tmp_now - last_updated.replace(tzinfo=None)
                                ) < timedelta(hours=24):
                                    if int(usd_price) != 0:
                                        usd_prices[erc20] = usd_price
                        no_prices = {}
                        symbols_string = ""

                        cmc_responses.update(response)

    return _lp_dict


def second_pass(_lp_dict) -> dict:
    # SECOND PASS:
    # 1. Loop through LP data and skip if False or one token is in USD contracts or eth contracts
    # 2. Check if either token has an ETH or USD price
    # 3. If they do have an ETH or USD price, mark LP as false if low equivalent liquidity

    for lp, lp_data in _lp_dict.items():
        if lp_data == False:
            # or (lp in SKIP_LPS)
            # or (lp_data["factory_address"] in SKIP_DEXS)
            continue
        elif lp_data["stable_pool"] == True:
            _lp_dict[lp] = False
            continue

        token0_address = lp_data["tokens"][0]
        token1_address = lp_data["tokens"][1]

        if (token0_address in USD_CONTRACTS) or (token1_address in USD_CONTRACTS):
            continue
            # because I've already checked it out
        elif (token0_address in ETH_CONTRACTS) or (token1_address in ETH_CONTRACTS):
            continue
            # because this was already checked and would be false if not enough liquidity

        elif (token0_address in usd_prices) or (token1_address in usd_prices):
            # if I grabbed the price on one of the tokens earlier in this loop, check liquidity with the price data
            # This may be redundant if I already checked it before, but it's okay for a second pass
            if (token0_address in usd_prices) and (
                usd_prices[token0_address]
                * (lp_data["reserves"][0] / (10 ** lp_data["token0"]["decimals"]))
            ) < AMMOUNT_USD:
                # if token0_quantity * USD_Price totals less than USD liquidity requirements, this is an invalid LP
                _lp_dict[lp] = False
                low_usd_lps[lp] = token0_address
                continue
            elif (token0_address in usd_prices) and (
                usd_prices[token0_address]
                * (lp_data["reserves"][0] / (10 ** lp_data["token0"]["decimals"]))
            ) >= AMMOUNT_USD:
                # the LP has sufficient liquidity so track the pools in erc20_pools
                build_erc20_pools(token0_address, lp)
                build_erc20_pools(token1_address, lp)
                lp_list.append({lp: [token0_address, token1_address]})
                continue

            elif (token1_address in usd_prices) and (
                usd_prices[token1_address]
                * (lp_data["reserves"][1] / (10 ** lp_data["token1"]["decimals"]))
            ) < AMMOUNT_USD:
                _lp_dict[lp] = False
                low_usd_lps[lp] = lp_data["tokens"][1]
                continue
            elif (token1_address in usd_prices) and (
                usd_prices[token1_address]
                * (lp_data["reserves"][1] / (10 ** lp_data["token1"]["decimals"]))
            ) >= AMMOUNT_USD:
                # the LP has sufficient liquidity so track the pools in erc20_pools
                build_erc20_pools(token0_address, lp)
                build_erc20_pools(token1_address, lp)
                lp_list.append({lp: [token0_address, token1_address]})
                continue

        elif (token0_address in eth_prices) or (token1_address in eth_prices):
            # again, check the token against ETH prices
            if (token0_address in eth_prices) and (
                lp_data["reserves"][0] / (10 ** lp_data["token0"]["decimals"])
            ) < AMMOUNT_ETH:
                _lp_dict[lp] = False
                low_usd_lps[str(lp)] = token0_address
                continue
            elif (token0_address in eth_prices) and (
                lp_data["reserves"][0] / (10 ** lp_data["token0"]["decimals"])
            ) >= AMMOUNT_ETH:
                # the LP has sufficient liquidity so track the pools in erc20_pools
                build_erc20_pools(token0_address, lp)
                build_erc20_pools(token1_address, lp)
                lp_list.append({lp: [token0_address, token1_address]})
                continue

            elif (token1_address in eth_prices) and (
                lp_data["reserves"][1] / (10 ** lp_data["token1"]["decimals"])
            ) < AMMOUNT_ETH:
                _lp_dict[lp] = False
                low_usd_lps[str(lp)] = token1_address
                continue
            elif (token1_address in eth_prices) and (
                lp_data["reserves"][1] / (10 ** lp_data["token1"]["decimals"])
            ) >= AMMOUNT_ETH:
                # the LP has sufficient liquidity so track the pools in erc20_pools
                build_erc20_pools(token0_address, lp)
                build_erc20_pools(token1_address, lp)
                lp_list.append({lp: [token0_address, token1_address]})
                continue

    return _lp_dict


def token_cleanup(_lps_dict) -> dict:
    for lp, data in _lps_dict.items():
        if _lps_dict[lp] != False:
            if ("token0" not in _lps_dict[lp]) or ("token1" not in _lps_dict[lp]):
                print(f"{lp} missing dictionary data")
                _lps_dict[lp] = False
                continue
            _lps_dict[lp]["token0"]["address"] = data["tokens"][0]
            _lps_dict[lp]["token1"]["address"] = data["tokens"][1]
    return _lps_dict


def main() -> None:
    # initialize variables
    start_time = perf_counter()
    lp_dict = {}

    path = "./reports"
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename, "*lp_dictionary.json"):
            print(filename)
            with open(os.path.join(path, filename), "r") as jfile:
                tmp_dict = json.load(jfile)
            tmp_dict = token_cleanup(tmp_dict)
            lp_dict.update(tmp_dict)

    # # Load LP JSON file
    # with open("reports/test.json", "r") as jfile:
    #     lp_dict = json.load(jfile)

    # First cleanup pass -- eliminate obvious low liquidity pools and build price dicts
    lp_dict = first_pass(lp_dict)
    # Second cleanup pass --check tokens against USD or ETH price and again eliminate low liquidity pools
    lp_dict = second_pass(lp_dict)

    # Write the cleaned-up LP dictionary to file as JSON
    tmp_json = json.dumps(lp_dict, indent=3)
    with open("reports/lps_dict.json", "w") as f_out:
        f_out.write(tmp_json)
    # Write the cleaned-up LP dictionary to file as JSON
    tmp_json = json.dumps(lp_list, indent=3)
    with open("reports/lps_list.json", "w") as f_out:
        f_out.write(tmp_json)
    # Write prices dicts
    tmp_json = json.dumps(usd_prices, indent=3)
    with open("reports/usd_prices.json", "w") as f_out:
        f_out.write(tmp_json)
    tmp_json = json.dumps(eth_prices, indent=3)
    with open("reports/eth_prices.json", "w") as f_out:
        f_out.write(tmp_json)

    # write ERC20_pools dictionary to possibly use when building triads
    tmp_json = json.dumps(erc20_pools, indent=3, default=serialize_sets)
    with open("reports/erc20_pools.json", "w") as f_out:
        f_out.write(tmp_json)

    # write all Coinmarketcap data that I obtained
    tmp_json = json.dumps(cmc_responses, indent=3)
    with open("reports/coinmarketcap_prices.json", "w") as jfile:
        jfile.write(tmp_json)

    # Write low liquidity LPs cause I might be able to scrape out some manual profits
    tmp_json = json.dumps(low_usd_lps, indent=3)
    with open("reports/low_usd_lps.json", "w") as f_out:
        f_out.write(tmp_json)
    tmp_json = json.dumps(low_eth_lps, indent=3)
    with open("reports/low_eth_lps.json", "w") as f_out:
        f_out.write(tmp_json)

    # Track runtime
    end_time = perf_counter()
    print(f"Completed in {end_time - start_time} seconds.")


if __name__ == "__main__":
    main()

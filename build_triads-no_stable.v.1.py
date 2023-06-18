from time import perf_counter
import json

# from brownie import config, network, interface


def main() -> None:
    # Load data from files
    with open("./reports/lps_dict.json", "r") as jfile:
        lp_dict = json.load(jfile)
    with open("./reports/erc20_pools.json", "r") as jfile:
        erc20_pools = json.load(jfile)
    # with open("factory_fee.json", "r") as jfile:
    #     fact_dict = json.load(jfile)

    # initialize variables
    triad_list = []
    output_list = []
    remove_duplicates_list = []
    tmp_check = False

    time_start = perf_counter()

    counter = 0
    for alpha_lp, pool_alpha in lp_dict.items():
        # counter += 1
        # if counter >= 30:
        #     break
        if pool_alpha != False:
            counter += 1
            print(f"Checking alpha LP #{counter}")
            # extract key data about alpha pair
            alpha_base_symbol = pool_alpha["token0"]["symbol"]
            alpha_quote_symbol = pool_alpha["token1"]["symbol"]
            alpha_pair_symbols = (
                alpha_base_symbol.upper() + "_" + alpha_quote_symbol.upper()
            )
            alpha_base_decimals = pool_alpha["token0"]["decimals"]
            alpha_quote_decimals = pool_alpha["token1"]["decimals"]
            alpha_base_contract = pool_alpha["tokens"][0]
            alpha_quote_contract = pool_alpha["tokens"][1]
            alpha_pair = alpha_base_contract + "_" + alpha_quote_contract
            alpha_tuple = (alpha_base_contract, alpha_quote_contract)
            alpha_pool_contract = alpha_lp
            alpha_pool_reserves = pool_alpha["reserves"]
            alpha_factory = pool_alpha["factory_address"]
            alpha_fee = pool_alpha["fee"]
            # (
            #     0.0
            #     if alpha_factory not in fact_dict
            #     else fact_dict[alpha_factory]["averageFee"]
            # )
            # alpha_router = (
            #     ""
            #     if alpha_factory not in fact_dict
            #     else fact_dict[alpha_factory]["router"]
            # )

            # find matching beta_pairs
            for beta_lp, pool_beta in lp_dict.items():
                if pool_beta != False:
                    # extract the beta pair data
                    beta_base_symbol = pool_beta["token0"]["symbol"]
                    beta_quote_symbol = pool_beta["token1"]["symbol"]
                    beta_pair_symbols = (
                        beta_base_symbol.upper() + "_" + beta_quote_symbol.upper()
                    )
                    beta_base_decimals = pool_beta["token0"]["decimals"]
                    beta_quote_decimals = pool_beta["token1"]["decimals"]
                    beta_base_contract = pool_beta["tokens"][0]
                    beta_quote_contract = pool_beta["tokens"][1]
                    beta_pair = beta_base_contract + "_" + beta_quote_contract
                    beta_tuple = (beta_base_contract, beta_quote_contract)
                    beta_pool_contract = beta_lp
                    beta_pool_reserves = pool_beta["reserves"]
                    beta_factory = pool_beta["factory_address"]
                    beta_fee = pool_beta["fee"]
                    # (
                    #     0.0
                    #     if beta_factory not in fact_dict
                    #     else fact_dict[beta_factory]["averageFee"]
                    # )
                    # beta_router = (
                    #     ""
                    #     if beta_factory not in fact_dict
                    #     else fact_dict[beta_factory]["router"]
                    # )

                    if (
                        (beta_base_contract in alpha_tuple)
                        or (beta_quote_contract in alpha_tuple)
                        and (alpha_pool_contract != beta_pool_contract)
                    ):
                        # set alpha_pair trade trade_direction in this potential triad
                        if alpha_quote_contract in beta_tuple:
                            # if alpha_quote is in the beta_pair, we trade alpha from base to quote (standard)
                            trade_direction = "0"
                        elif alpha_base_contract in beta_tuple:
                            trade_direction = "1"
                        # set beta_pair trade trade_direction in this potential triad
                        if beta_base_contract in alpha_tuple:
                            # IF BETA_PAIR ONLY HAS ONE CONTRACT:
                            if beta_quote_contract in erc20_pools:
                                if len(erc20_pools[beta_quote_contract]) <= 1:
                                    # print(
                                    #     f"{beta_quote_contract} only has {beta_lp} as a contract.  Move along."
                                    # )
                                    continue
                            # if beta_base is in the alpha_pair, we would have just traded into it, so we trade beta_pair from base to quote
                            trade_direction = trade_direction + "-0"
                            alpha_beta_shared_token = beta_base_contract
                        elif beta_quote_contract in alpha_tuple:
                            # if we just traded to beta_quote, we need to trade from beta_quote to beta_base
                            trade_direction = trade_direction + "-1"
                            alpha_beta_shared_token = beta_quote_contract
                            if beta_base_contract in erc20_pools:
                                if len(erc20_pools[beta_base_contract]) <= 1:
                                    # print(
                                    #     f"{beta_base_contract} only has {beta_lp} as a contract.  Move along."
                                    # )
                                    continue
                        # find matching beta_pairs
                        for gamma_lp, pool_gamma in lp_dict.items():
                            if pool_gamma != False:
                                # extract the beta pair data
                                gamma_base_symbol = pool_gamma["token0"]["symbol"]
                                gamma_quote_symbol = pool_gamma["token1"]["symbol"]
                                gamma_pair_symbols = (
                                    gamma_base_symbol.upper()
                                    + "_"
                                    + gamma_quote_symbol.upper()
                                )
                                gamma_base_decimals = pool_gamma["token0"]["decimals"]
                                gamma_quote_decimals = pool_gamma["token1"]["decimals"]
                                gamma_base_contract = pool_gamma["tokens"][0]
                                gamma_quote_contract = pool_gamma["tokens"][1]
                                gamma_pair = (
                                    gamma_base_contract + "_" + gamma_quote_contract
                                )
                                gamma_tuple = (
                                    gamma_base_contract,
                                    gamma_quote_contract,
                                )
                                gamma_pool_contract = gamma_lp
                                gamma_pool_reserves = pool_gamma["reserves"]
                                gamma_factory = pool_gamma["factory_address"]
                                gamma_fee = pool_gamma["fee"]
                                # (
                                #     0.0
                                #     if gamma_factory not in fact_dict
                                #     else fact_dict[gamma_factory]["averageFee"]
                                # )
                                # gamma_router = (
                                #     ""
                                #     if gamma_factory not in fact_dict
                                #     else fact_dict[gamma_factory]["router"]
                                # )

                                if (
                                    (gamma_base_contract in beta_tuple)
                                    and (gamma_pool_contract != alpha_pool_contract)
                                    and (
                                        gamma_quote_contract != alpha_beta_shared_token
                                    )
                                    and (gamma_base_contract != alpha_beta_shared_token)
                                    and (gamma_pool_contract != beta_pool_contract)
                                    and (gamma_quote_contract in alpha_tuple)
                                ):
                                    tmp_direction = trade_direction
                                    trade_direction = trade_direction + "-0"
                                    tmp_check = True
                                elif (
                                    (gamma_quote_contract in beta_tuple)
                                    and (gamma_pool_contract != alpha_pool_contract)
                                    and (
                                        gamma_quote_contract != alpha_beta_shared_token
                                    )
                                    and (gamma_base_contract != alpha_beta_shared_token)
                                    and (gamma_pool_contract != beta_pool_contract)
                                    and (gamma_base_contract in alpha_tuple)
                                ):
                                    tmp_direction = trade_direction
                                    trade_direction = trade_direction + "-1"
                                    tmp_check = True

                                tmp_triad = (
                                    alpha_pool_contract
                                    + ","
                                    + beta_pool_contract
                                    + ","
                                    + gamma_pool_contract
                                )

                                if (tmp_check == True) and not (
                                    tmp_triad in remove_duplicates_list
                                ):
                                    # if there is a complete and valid trade path from alpha -> beta -> gamma -> alpha
                                    # and if the set wasn't already done, build out the triad data set
                                    remove_duplicates_list.append(tmp_triad)
                                    tmp_list = (
                                        alpha_pool_contract
                                        + ","
                                        + beta_pool_contract
                                        + ","
                                        + gamma_pool_contract
                                        + ","
                                        + trade_direction
                                    )
                                    # (
                                    # alpha_pair_symbols
                                    # + ","
                                    # + beta_pair_symbols
                                    # + ","
                                    # + gamma_pair_symbols
                                    # + ","
                                    # + trade_direction
                                    # )
                                    output_list.append(tmp_list)

                                    # build triad
                                    output_dict = {
                                        "alphaPair": alpha_pair,
                                        "alphaPairSymbols": alpha_pair_symbols,
                                        "alphaBaseSymbol": alpha_base_symbol,
                                        "alphaQuoteSymbol": alpha_quote_symbol,
                                        "alphaBaseContract": alpha_base_contract,
                                        "alphaQuoteContract": alpha_quote_contract,
                                        "alphaBaseDecimals": alpha_base_decimals,
                                        "alphaQuoteDecimals": alpha_quote_decimals,
                                        "alphaPoolContract": alpha_pool_contract,
                                        "alphaPoolReserves": alpha_pool_reserves,
                                        "alphaFactory": alpha_factory,
                                        "alphaFee": alpha_fee,
                                        # "alphaRouter": alpha_router,
                                        "betaPair": beta_pair,
                                        "betaPairSymbols": beta_pair_symbols,
                                        "betaBaseSymbol": beta_base_symbol,
                                        "betaQuoteSymbol": beta_quote_symbol,
                                        "betaBaseContract": beta_base_contract,
                                        "betaQuoteContract": beta_quote_contract,
                                        "betaBaseDecimals": beta_base_decimals,
                                        "betaQuoteDecimals": beta_quote_decimals,
                                        "betaPoolContract": beta_pool_contract,
                                        "betaPoolReserves": beta_pool_reserves,
                                        "betaFactory": beta_factory,
                                        "betaFee": beta_fee,
                                        # "betaRouter": beta_router,
                                        "gammaPair": gamma_pair,
                                        "gammaPairSymbols": gamma_pair_symbols,
                                        "gammaBaseSymbol": gamma_base_symbol,
                                        "gammaQuoteSymbol": gamma_quote_symbol,
                                        "gammaBaseContract": gamma_base_contract,
                                        "gammaQuoteContract": gamma_quote_contract,
                                        "gammaBaseDecimals": gamma_base_decimals,
                                        "gammaQuoteDecimals": gamma_quote_decimals,
                                        "gammaPoolContract": gamma_pool_contract,
                                        "gammaPoolReserves": gamma_pool_reserves,
                                        "gammaFactory": gamma_factory,
                                        "gammaFee": gamma_fee,
                                        # "gammaRouter": gamma_router,
                                        "triadPairSymbols": alpha_pair_symbols
                                        + "->"
                                        + beta_pair_symbols
                                        + "->"
                                        + gamma_pair_symbols,
                                        "tradeDirections": trade_direction,
                                    }
                                    triad_list.append(output_dict)

                                    # Reset tmp_check so it doesn't cary over to the next iteration
                                    tmp_check = False
                                    # Reset so I don't keep adding onto the direction for the alpha-beta set
                                    trade_direction = tmp_direction

    time_end = perf_counter()
    total_time = (time_end - time_start) / 60
    print(f"Completed in {total_time} minutes.")

    with open("./reports/triadsList.txt", "w") as triad_list_file:
        triad_list_file.write("\n".join(output_list))
    with open("./reports/triadsList.json", "w") as triad_json_file:
        json.dump(triad_list, triad_json_file)
    return triad_list


if __name__ == "__main__":
    main()

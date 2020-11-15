from brownie import *
import time


# KWH Protocol Constants
TOKEN_ADDRESS = '0x78B57C213a18DF1DAbC647149902ea1966E0119C'
TOKEN_WETH_PAIR = '0x2350A783EFEB9322631f6b87fDeBEb1852AD346D'
# WETH mainnet address
# WETH_ADDRESS = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2' # mainnet
WETH_ADDRESS = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'  # goerli


def deploy_uniswap_zap():
    uniswap_zap = UniswapZAP.deploy({"from": accounts[0]})
    # initUniswapZAP(address token, address WETH, address tokenWethPair)
    uniswap_zap.initUniswapZAP(TOKEN_ADDRESS, WETH_ADDRESS, TOKEN_WETH_PAIR, {"from": accounts[0]})
    print("UniswapZAP contract deployed at: " + str(uniswap_zap))
    return uniswap_zap


def main():
    if network.show_active() == 'mainnet':
        # replace with your keys
        accounts.load("liquidityzap")

    if network.show_active() in ['goerli']:
        # your address
        accounts.add('your_private_key')
        
    # Create Uniswap Liquidity Zap
    uniswap_zap = deploy_uniswap_zap()
    



# brownie run deploy_UniswapZAP.py --network mainnet
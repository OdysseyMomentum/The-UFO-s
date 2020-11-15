from brownie import *
import time


# KWH Protocol Constants
TOKEN_ADDRESS = '0x78B57C213a18DF1DAbC647149902ea1966E0119C'
TOKEN_WETH_PAIR = '0x2350A783EFEB9322631f6b87fDeBEb1852AD346D'
# WETH_ADDRESS = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
WETH_ADDRESS = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'
TENPOW18 = 10 ** 18

# Uniswap 
#ZAP_ADDRESS = '0x3DF62cE0989Ea78aDcc2b1E338c84A57F70f1e4E'
ZAP_ADDRESS = '0x657ED9608218cbbAd40cE9D15C60a0494fd228fd'


def get_zap():
    uniswap_zap = UniswapZAP.at(ZAP_ADDRESS)
    print("UniswapZAP contract deployed at: " + str(uniswap_zap))
    return uniswap_zap

def get_lp(uniswap_zap, liquidity):
    lp = uniswap_zap.getLPTokenPerEthUnit(liquidity, {"from": accounts[0]})
    print(lp)

def main():
    if network.show_active() == 'mainnet':
        # replace with your keys
        accounts.load("liquidityzap")
    if network.show_active() in ['goerli']:
        # 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')
        # 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')

    liquidity_to_add = 0.001 * TENPOW18

    # Create Uniswap Liquidity Zap
    liquidity_zap = get_zap()
    print(get_lp(liquidity_zap, liquidity_to_add))
    print(get_lp(liquidity_zap, 10*liquidity_to_add))
    print(get_lp(liquidity_zap, 100*liquidity_to_add))
    #liquidity_zap.addLiquidityETHOnly(accounts[0], {"from": accounts[0], "value": liquidity_to_add} )


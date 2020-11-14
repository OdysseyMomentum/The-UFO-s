import os
os.environ['PROVIDER'] = 'https://goerli.prylabs.net/'
#os.environ['PROVIDER'] = 'https://main-rpc.linkpool.io'
import time

from uniswap import Uniswap
address = "0xFe594E862c3ce76E192997EABFC41Afd7C975b52"
private_key = "3a8bb854c7a86d950c0d3e0b5b1bbcd3912389a95fa530e46c911fe1de099808"  # or None, if you're not going to make transactions

uniswap_wrapper = Uniswap(address, private_key, version=2)  # pass version=2 to use Uniswap v2

eth = "0x0000000000000000000000000000000000000000"
weth = uniswap_wrapper.w3.toChecksumAddress("0xb4fbf271143f4fbf7b91a5ded31805e42b2208d6")
kwh = uniswap_wrapper.w3.toChecksumAddress("0x78B57C213a18DF1DAbC647149902ea1966E0119C")

amount = 1*10**18

# Recursive function to get the price to the  plus minus 2 percent range within price
def bump_price(target_price_cents):

	eth_bal = uniswap_wrapper.get_eth_balance()
	kwh_bal = uniswap_wrapper.get_token_balance(kwh)

	# current price ETH per one unit of KWH
	current_price = uniswap_wrapper.get_token_token_input_price(kwh, weth, amount)/10**18	
	current_price_cents = current_price * 400 * 100

	print('current price eth {}'.format(current_price))
	print('current price cents {}'.format(current_price_cents))
	
	# the price we expect to see ETH per unit KWH
	target_price = target_price_cents / 40000

	# we need to buy KWH
	if target_price > 1.02*current_price:
		print("Current price of KWH too low", '\n')
		percentage = 0.01
		uniswap_wrapper.make_trade(eth, kwh, int(eth_bal*percentage))

	elif target_price <= 1.02*current_price and target_price >= 0.98*current_price:
		print('Target price within range', '\n')
		return

	# we need to buy ETH
	elif target_price < 0.98*current_price:
		print("Current price of KWH too high", '\n')
		percentage = 0.01
		uniswap_wrapper.make_trade(kwh, eth, int(kwh_bal*percentage))
	time.sleep(30)

	return bump_price(target_price_cents)

'''
bump_price(20)

eth_bal = uniswap_wrapper.get_eth_balance()
kwh_bal = uniswap_wrapper.get_token_balance(kwh)

# current price ETH per one unit of KWH
current_price = uniswap_wrapper.get_token_token_input_price(kwh, weth, amount)/10**18	
current_price_cents = current_price * 400 * 100

print('current price eth {}'.format(current_price))
print('current price cents {}'.format(current_price_cents))
'''


import os
os.environ['PROVIDER'] = 'https://goerli.prylabs.net/'
#os.environ['PROVIDER'] = 'https://main-rpc.linkpool.io'
import time
import logging
logging.basicConfig(filename='my.log', level=logging.INFO)

from uniswap import Uniswap
address = "0xFe594E862c3ce76E192997EABFC41Afd7C975b52"
private_key = "3a8bb854c7a86d950c0d3e0b5b1bbcd3912389a95fa530e46c911fe1de099808"  # or None, if you're not going to make transactions

uniswap_wrapper = Uniswap(address, private_key, version=2)  # pass version=2 to use Uniswap v2

eth = "0x0000000000000000000000000000000000000000"
weth = uniswap_wrapper.w3.toChecksumAddress("0xb4fbf271143f4fbf7b91a5ded31805e42b2208d6")
kwh = uniswap_wrapper.w3.toChecksumAddress("0x78B57C213a18DF1DAbC647149902ea1966E0119C")

amount = 1*10**18

def wait_for_tx(tx_hash):
	try:
		uniswap_wrapper.w3.getTransactionReceipt(tx_hash)
	except web3.exceptions.TransactionNotFound:
		wait_for_tx(tx_hash)

# Recursive function to get the price to the  plus minus 2 percent range within price
def bump_price(target_price_cents):

	eth_bal = uniswap_wrapper.get_eth_balance()
	kwh_bal = uniswap_wrapper.get_token_balance(kwh)

	# current price ETH per one unit of KWH
	current_price = uniswap_wrapper.get_token_token_input_price(kwh, weth, amount)/10**18	
	current_price_cents = current_price * 400 * 100

	logging.info('current price eth {}'.format(current_price))
	logging.info('current price cents {}'.format(current_price_cents))
	
	# the price we expect to see ETH per unit KWH
	target_price = target_price_cents / 40000

	# we need to buy KWH
	if target_price > 1.02*current_price:
		logging.info("Current price of KWH too low")
		amount_to_sell_eth = eth_bal*(target_price - current_price)/(current_price + target_price)
		tx = uniswap_wrapper.make_trade(eth, kwh, int(amount_to_sell_eth)).hex()
		logging.info(tx)
		uniswap_wrapper.w3.eth.waitForTransactionReceipt(tx)
		return bump_price(target_price_cents)

	elif target_price <= 1.02*current_price and target_price >= 0.98*current_price:
		logging.info('Target price within range')

		logging.info('Bump successful!')

	# we need to buy ETH
	elif target_price < 0.98*current_price:
		logging.info("Current price of KWH too high")
		amount_to_sell_kwh = kwh_bal*(current_price - target_price)/(current_price + target_price)
		tx = uniswap_wrapper.make_trade(kwh, eth, int(amount_to_sell_kwh)).hex()
		logging.info(tx)
		uniswap_wrapper.w3.eth.waitForTransactionReceipt(tx)
		return bump_price(target_price_cents)
	else:
		logging.info('Could not bump price')
	

	

'''
bump_price(20) # test one price bump

# Swap one KWH
tx = uniswap_wrapper.make_trade(kwh, eth, int(1*10**18)).hex()
print(tx)
uniswap_wrapper.w3.eth.waitForTransactionReceipt(tx)
'''
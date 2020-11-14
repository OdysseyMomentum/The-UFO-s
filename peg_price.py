from utils.uniswap_functions import *
import logging

with open('Datasets/oracle-data/Balancing_prices_aligned_non_negative_2020-10-17-2020-11-31.csv') as oracle:
	lines = oracle.readlines()
	for line in lines[1:6]:
		target_price = round(float(line.split(';')[0].split(',')[1])*100/1000, 4)
		logging.info('Target price: {} cents'.format(target_price))
		
		# Uncomment the line below to see the bumps in action
		#bump_price(target_price)
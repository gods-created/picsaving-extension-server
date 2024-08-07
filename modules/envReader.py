import os
from loguru import logger

def read():
	path = './.env'
	if not os.path.exists(path):
		logger.error('.env file not exists!')
		return

	with open(path, 'r') as f:
		env = f.readlines()

	key_value_pairs = {pair.split('=')[0]: pair.split('=')[1].replace('\n', '').strip() for pair in env}

	return key_value_pairs


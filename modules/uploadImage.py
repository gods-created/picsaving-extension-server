import unittest
import requests
import base64
import boto3
import string
import random
import io
import re
from loguru import logger
import modules.envReader as envReader

class Singleton(type):
	_inst = None

	def __new__(cls, name, based, dct):
		return super().__new__(cls, name, based, dct)

	def __call__(cls, *args, **kwargs):
		if cls._inst is None:
			cls._inst = super().__call__(*args, **kwargs)

		return cls._inst

class UploadImage(metaclass=Singleton):
	def __new__(cls, *args, **kwargs):
		return super().__new__(cls, *args, **kwargs)

	def __init__(self):
		pass

	@classmethod
	def __if_url(cls, url):
		pattern = r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$'
		return re.match(pattern, url) is not None

	@classmethod
	def __s3_bucket(cls):
		env = envReader.read()
		if not isinstance(env, dict):
			return '.env file not exists!'

		aws_access_key_id = env.get('AWS_ACCESS_KEY_ID')
		aws_secret_access_key = env.get('AWS_SECRET_ACCESS_KEY')
		s3_bucket_name = env.get('S3_BUCKET_NAME')

		s3_client = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
		s3_bucket = s3_client.Bucket(s3_bucket_name)

		return s3_bucket	

	@classmethod
	def __generate_filename(cls):
		random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(25))
		return f'{random_string}.png'

	@classmethod
	def run(cls, url):
		response_json = {
			'status': 'error',
			'err_description': ''
		}

		try:
			if not cls.__if_url(url):
				response_json['err_description'] = 'This is not URL!'
				logger.info(response_json)
				return response_json

			request = requests.request('GET', url)
			if request.status_code != 200:
				response_json['err_description'] = f'Request error: {request.status_code}!'
				logger.info(response_json)
				return response_json

			content = request.content
			bytes_image = io.BytesIO(content)
			bytes_image.seek(0)
			filename = cls.__generate_filename()

			s3_bucket = cls.__s3_bucket()

			try:
				upload_fileobj = s3_bucket.upload_fileobj(bytes_image, Key=filename)
				response_json['status'] = 'success'
				
			except:
				response_json['err_description'] = s3_bucket

		except Exception as e:
			response_json['err_description'] = str(e)

		logger.info(response_json)
		return response_json
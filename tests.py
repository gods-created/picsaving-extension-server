import unittest
from modules.uploadImage import UploadImage

class Tests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		pass

	def setUp(self):
		self.url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREoRGyXmHy_6aIgXYqWHdOT3KjfmnuSyxypw&s'

	def testUploadImage(self):
		url = self.url
		run_response = UploadImage.run(url)
		status = run_response.get('status', 'error')

		self.assertEqual(status, 'success')

	def tearDown(self):
		pass 

	@classmethod
	def tearDownClass(cls):
		pass

if __name__ == '__main__':
	unittest.main()
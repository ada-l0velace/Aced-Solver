import wolframalpha
from threading import Thread

class WolframRequests():
	"""
	Handles all API Wolfram Querys
	"""

	def __init__(self, app_id):
		self.client = wolframalpha.Client(app_id)
		self.query = ""
		self.response = ""
		self.t = None

	def request(self):
		self.response = self.client.query(self.query)

	def get_pod(self):
		return self.response.pods

	def run (self, data):
		self.query = data
		self.t = Thread(target=self.request)
		self.t.start()

	def join(self):
		self.t.join()

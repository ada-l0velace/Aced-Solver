import wolframalpha
from threading import Thread, Lock

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


class AcedSolverRequests():
	"""
	Handles all Wolfram Requests Clients
	"""

	def __init__(self, clients):
		self.clients = clients
		self.t = []
		self.mutex = Lock()

	def request(self, client):
		client.run()
		with self.mutex:
			print '--------------------------------------------------------------------------'
			print client
	def get_pod(self):
		return self.response.pods

	def run (self):
		i = 0
		for client in self.clients:
			self.t.append(Thread(target=self.request, args=[client]))
			self.t[i].start()
			i += 1
		for t in self.t:
			t.join()
		print 'Today was a great day for Science'

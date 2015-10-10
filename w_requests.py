from threading import Thread, Lock
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, auto_number, convert_xor
transformations = (standard_transformations +(implicit_multiplication_application,convert_xor, ))


class SymPyRequests():
	"""
	Handles all SymPy Querys
	"""

	def __init__(self):
		self.args = []
		self.query = None
		self.response = None
		self.t = None
		self.function = None

	def get_response(self):
		return unicodeself.response

	def request(self):
		self.response = self.function(*self.args)

	def run (self, query, function, args):
		self.query = query
		self.function = function
		self.args = args
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
			print client
			print '------------------------------------------------------------------------------------'
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

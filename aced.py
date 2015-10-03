from abc import ABCMeta, abstractmethod
from w_requests import WolframRequests
from prettytable import PrettyTable

class BaseAced():
	"""
	Base Class for all Aced Classes
	"""
	__metaclass__ = ABCMeta
	wolfram_request = []

	def set_requests(self, app_id):
		self.wolfram_request = []
		for query in self.querys:
			self.wolfram_request.append(WolframRequests(app_id))

	@abstractmethod
	def run (self):
		i = 0
		for query in self.querys:
			self.wolfram_request[i].run(query)	
			i += 1
		for r in self.wolfram_request:
			r.join()


class Holomorph(BaseAced):
	"""
	Checks if a function is Holomorph
	"""

	def __init__(self, func, app_id):
		self.func = func
		self.dudx = 'd/dx(Re(%s))' % func
		self.dudy = 'd/dy(Re(%s))' % func
		self.dvdx = 'd/dx(Im(%s))' % func
		self.dvdy = 'd/dy(Im(%s))' % func
		self.querys = [self.dudx,self.dudy,self.dvdx,self.dvdy]
		self.set_requests(app_id)
		self.answer = False
		self.matrix = ""

	def __str__(self):
		if(self.answer):
			print self.matrix
			return "The function %s is Holomorph\n" % self.func 

		return "The function %s isn't Holomorph" % self.func

	def matrix_r(self, matrix):
		p = PrettyTable()
		for row in matrix:
			p.add_row(row)
		self.matrix = p.get_string(header=False, border=False)

	def run (self):
		super(Holomorph,self).run()
		dudx = self.wolfram_request[0].get_pod()[4].text
		dvdy = self.wolfram_request[3].get_pod()[4].text
		dxdy = self.wolfram_request[1].get_pod()[4].text
		dvdx = self.wolfram_request[2].get_pod()[4].text
		self.matrix_r([[dudx,dxdy],[dvdx,dvdy]])
		self.answer = dudx == dvdy and dxdy == '-%s' % dvdx
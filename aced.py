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


class SimpleOperation(BaseAced):
	"""
	Class to make simple operations
	"""

	def __init__(self, func, app_id):
		self.func = func
		self.querys = [func]
		self.set_requests(app_id)
		self.answer = False
		self.value = []

	def __str__(self):
		if(self.answer):
			return "The answer is %s" % self.value 
		return "An error ocurred"

	def run (self):
		super(SimpleOperation,self).run()
		self.value = self.wolfram_request[0].get_pod()[1].text
		self.answer = True


class PathIntegral(BaseAced):
	"""
	Class to perform path integrals
	"""

	def __init__(self, func, path, irange, app_id):
		self.app_id = app_id
		self.path = path
		self.t = '%s at z=%s' % (func,path)
		self.dt = 'd/dt(%s)' % path
		self.integral = 'Integrate[(%s)+(%s), {t, %d, %d}]'
		self.range = irange
		self.func = func
		self.querys = [self.t, self.dt]
		self.set_requests(app_id)
		self.answer = False
		self.value = ""

	def __str__(self):
		if(self.answer):
			return "%s" % self.value 
		return "An error ocurred"

	def run_last(self, t, dt):
		r = WolframRequests(self.app_id)
		r.run('Integrate[(%s)(%s), {t, %d, %d}]' % (t, dt, self.range[0],self.range[1]))
		r.join()
		self.value = "f(t) = %s\nf'(t) = %s\n%s" % (t,dt,r.get_pod()[0].text[1:])
		self.answer = True
		
	def run (self):
		super(PathIntegral,self).run()
		t = self.wolfram_request[0].get_pod()[3].text
		dt = self.wolfram_request[1].get_pod()[0].text.split(' = ')[1]
		self.run_last(t,dt)
		#self.value = self.wolfram_request[0].get_pod()[1].text
		
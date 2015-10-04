from abc import ABCMeta, abstractmethod
from w_requests import WolframRequests
from prettytable import PrettyTable
import unicodedata
import re

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
		self.value = ""

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

class IntegralCauchyFormula(BaseAced):
	"""
	Calculates a integral with cauchy formula
	"""

	def __init__(self, numerator, denominator, app_id):
		#"d/dz(-(2i-2)(z-3i-4)^(3)+(3i-1)z^(2)) at z =2i+5"
		self.app_id = app_id
		self.denominator = denominator
		self.numerator = numerator
		self.roots = []
		self.querys = ["%s = 0" % (denominator)]
		self.set_requests(app_id)
		self.answer = False
		self.value = ""

	def __str__(self):
		if(self.answer):
			return unicodedata.normalize('NFD', self.value).encode('ascii', 'ignore') 
		return "An error ocurred"

	def extra_runs(self, splited_n):
		self.querys = []
		self.wolfram_request = []
		dicti = {}
		dicti_rev = {}
		not_splited = ""
		for z in range(len(splited_n)):
			not_splited += splited_n[z]
		not_splited = not_splited.replace(' = 0','')
		splited_n[-1] = splited_n[-1].replace(' = 0','')
		degrees = []
		nr_d = []
		if '^' in not_splited:
			for i in range(len(splited_n)):
				if ')^' in splited_n[i]:
					nr_d.append(i)
					degrees.append(int(re.sub('[!^]', '', splited_n[i].split('^')[1])))
					print degrees[i]
		for i in range(len(splited_n)):
			dicti[splited_n[i]] = self.roots[i]
			dicti_rev[self.roots[i]] = splited_n[i]
		den_new = not_splited
		i = 0
		for root in self.roots:

			den_new = not_splited
			alpha_d = den_new.replace (dicti_rev[root],"(1)")
			if i not in nr_d:
				self.querys.append("(%s)/(%s) at z = %s" % (self.numerator, alpha_d, root))
			elif degrees[i]-1 == 0:
				self.querys.append("(%s)/(%s) at z = %s" % (self.numerator, alpha_d, root))
			elif degrees[i]-1 == 1:
				print "d^/dz(%s)/(%s) at z = %s" % (self.numerator, alpha_d, root)
				self.querys.append("d/dz(%s)/(%s) at z = %s" % (self.numerator, alpha_d, root))
			elif degrees[i]-1 > 1:
				print "d^%d/dz^%d(%s)/(%s) at z = %s" % (degrees[i]-1,degrees[i]-1,self.numerator, alpha_d, root)
				self.querys.append("d^%d/dz^%d(%s)/(%s) at z = %s" % (degrees[i]-1,degrees[i]-1,self.numerator, alpha_d, root))
			i += 1
		self.set_requests(self.app_id)
		super(IntegralCauchyFormula,self).run()
		for wfr in self.wolfram_request:
			for pod in wfr.get_pod():
				self.value += "\n%s\n" % pod.title
				for subpod in pod.subpods:
					self.value += "%s\n%s\n" % (subpod.text, subpod.img.attrib['src'])
		

	def run (self):
		super(IntegralCauchyFormula,self).run()
		sols = ['Complex solutions', 'Real solutions', 'Complex solution', 'Real solution']
		splited_n = self.wolfram_request[0].get_pod()[0].text.split(') (')
		for i in range(len(splited_n)-1):
			if i == 0:
				splited_n[i] += ')'
			else:
				splited_n[i] = '(' + splited_n[i] + ')'
		splited_n[-1] = '(' + splited_n[-1] 
		for pod in self.wolfram_request[0].get_pod():
			if pod.title in sols:
				self.value += "\n%s\n" % pod.title
				for subpod in pod.subpods:
					self.roots.append(subpod.text.split(' = ')[1])
					self.value += "%s\n%s\n" % (subpod.text, subpod.img.attrib['src'])
		self.roots = list(reversed(self.roots))
		self.extra_runs(splited_n)
		#self.value = self.wolfram_request[0].get_pod()[4].text
		self.answer = True



class DerevativePoint(BaseAced):
	"""
	Calculates the derevative on a specific point
	"""

	def __init__(self, func, point, app_id):
		#"d/dz(-(2i-2)(z-3i-4)^(3)+(3i-1)z^(2)) at z =2i+5"
		self.func = func
		self.querys = ["d/dz(%s) at z =%s" % (func,point)]
		self.set_requests(app_id)
		self.answer = False
		self.value = ""

	def __str__(self):
		if(self.answer):
			return "The answer is %s" % self.value 
		return "An error ocurred"

	def run (self):
		super(DerevativePoint,self).run()
		self.value = self.wolfram_request[0].get_pod()[1].text
		self.answer = True


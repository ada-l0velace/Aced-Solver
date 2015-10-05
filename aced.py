from abc import ABCMeta, abstractmethod
from w_requests import WolframRequests
from prettytable import PrettyTable
import unicodedata
import re

class bcolors:
	"""
	Class to use Colors in terminal
	"""
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


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
			print "%sCalculating %s %s" % (bcolors.OKBLUE,query, bcolors.ENDC)
			self.wolfram_request[i].run(query)	
			i += 1
		for r in self.wolfram_request:
			r.join()


class Holomorph(BaseAced):
	"""
	Checks if a function is Holomorph
	"""

	def __init__(self, real, imaginary, app_id):
		self.app_id = app_id
		self.func = "(%s) + (%s) i" % (real, imaginary)
		self.real = real.replace('y', 't')
		self.imaginary = imaginary.replace('y', 't')
		self.dudx = 'D[%s,x]' % self.real
		self.dudy = 'D[%s,t]' % self.real
		self.dvdx = 'D[%s,x]' % self.imaginary
		self.dvdy = 'D[%s,t]' % self.imaginary
		self.querys = [self.dudx,self.dudy,self.dvdx,self.dvdy]
		self.set_requests(app_id)
		self.answer = False
		self.matrix = ""

	def __str__(self):
		print 'Jacobiana'
		print self.matrix
		print ''
		if(self.answer):
			return bcolors.OKGREEN+"The function %s + (%s)i is Holomorph" % (self.real.replace('t', 'y'), self.imaginary.replace('t', 'y'))+bcolors.ENDC 

		return bcolors.FAIL+"The function %s + (%s)i isn't Holomorph" % (self.real.replace('t', 'y'), self.imaginary.replace('t', 'y'))+bcolors.ENDC

	def matrix_r(self, matrix):
		p = PrettyTable()
		for row in matrix:
			p.add_row(row)
		self.matrix = p.get_string(header=False, border=False)

	def run (self):
		super(Holomorph,self).run()
		results = []
		dd = []
		wr_n = 0
		for wr in self.wolfram_request:
			for pod in wr.get_pod():
				if pod.title == 'Alternate forms' or pod.title == 'Alternate form':
					dd.append(pod.text)
		self.wolfram_request = []
		self.querys = ["(%s) == (%s)" % (dd[0],dd[3]), "(-1)(%s) == (%s)" % (dd[1],dd[2])]
		self.set_requests(self.app_id)
		super(Holomorph,self).run()
		for wr in self.wolfram_request:
			f = False	
			for pod in wr.get_pod():
				if pod.text == 'True':
					results.append(pod.text)
					f = True
					break
			if not f:
				results.append('False')
		if (results[0] == 'True' and results[1] == 'True'):
			self.answer = True	
		self.matrix_r([[dd[0],dd[1]],[dd[2],dd[3]]])
		
		

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

	def __init__(self, numerator, denominator,center, ray, app_id):
		#"d/dz(-(2i-2)(z-3i-4)^(3)+(3i-1)z^(2)) at z =2i+5"
		self.center = center
		self.ray = ray
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

	def reset_querys(self):
		self.querys = []
		self.wolfram_request = []

	def is_singularity_on_center(self):
		self.reset_querys()
		for singularity in self.roots:
			self.querys.append('Re(%s)' % singularity)
			self.querys.append('Im(%s)' % singularity)
		self.querys.append('Re(%s)' % self.center)
		self.querys.append('Im(%s)' % self.center)
		self.set_requests(self.app_id)
		super(IntegralCauchyFormula, self).run()
		i = 0
		z = 0
		points = []
		for wr in self.wolfram_request:		
			for pod in wr.get_pod():
				if pod.title == 'Result':
					points.append([])
					if i % 2 == 0 and i != 0:
						z += 1
					points[z].append(pod.text)
					i += 1
		points = points[:i/2]
		center = points[-1]
		points.pop()
		self.reset_querys()
		for point in points:
			centerX = center[0]
			centerY = center[1]
			pointX = point[0]
			pointY = point[1]
			equation = "((%s) - (%s))^2 + ((%s) - (%s))^2 < (%s)^2" % (pointX, centerX, pointY, centerY, self.ray)
			self.querys.append(equation)
		self.set_requests(self.app_id)
		super(IntegralCauchyFormula, self).run()
		i = 0
		self.roots_in_circunference = []
		for wr in self.wolfram_request:		
			for pod in wr.get_pod():
				if pod.text == 'True':
					self.roots_in_circunference.append(self.roots[i])

			i += 1

	def extra_runs(self, splited_n):
		dicti = {}
		dicti_rev = {}
		not_splited = ""
		for z in range(len(splited_n)):
			not_splited += splited_n[z]
		not_splited = not_splited.replace(' = 0','')
		splited_n[-1] = splited_n[-1].replace(' = 0','')
		degrees = []
		nr_d = []
		
		den_new = not_splited
		n_den = []
		
		"""
		for singularity in splited_n:
			self.querys.append('simplify[%s]' % singularity)	
		self.set_requests(self.app_id)
		super(IntegralCauchyFormula,self).run()
		
		for wr in self.wolfram_request:
			for pod in wr.get_pod():
				i = 0
				if pod.title == 'Results':
					for subpod in pod.subpods:
						if i == int(pod.numsubpods)-1:
							print subpod.text
							m = subpod.text.split(' ')
							for z in m:
								n_den.append(z)
						i += 1
				elif pod.title == 'Result':
					n_den.append('(%s)' % pod.text)
		"""
		
		for root in self.roots:
			n_den.append('z -(%s)' % root)
		#print splited_n
		self.reset_querys()
		for den in splited_n:
			self.querys.append('Exponent[(%s),z]' % den)
		self.set_requests(self.app_id)
		super(IntegralCauchyFormula,self).run()
		for wr in self.wolfram_request:		
			for pod in wr.get_pod():
				if pod.title == 'Result':
					degrees.append(int(pod.text))
		for i in range(len(n_den)):
			dicti_rev[self.roots[i]] = n_den[i]
		not_splited = ""
		for s in n_den:
			not_splited += s
		self.reset_querys()
		i = 0
		self.is_singularity_on_center()
		self.reset_querys()
		for root in self.roots_in_circunference:
			den_new = not_splited
			alpha_d = den_new.replace (dicti_rev[root],"(1)")
			if degrees[i]-1 == 0:
				self.querys.append("(%s)/(%s) at z = %s" % (self.numerator, alpha_d, root))
			elif degrees[i]-1 == 1:
				#print "d^/dz(%s)/(%s) at z = %s" % (self.numerator, alpha_d, root)
				self.querys.append("d/dz(%s)/(%s) at z = %s" % (self.numerator, alpha_d, root))
			elif degrees[i]-1 > 1:
				#print "d^%d/dz^%d(%s)/(%s) at z = %s" % (degrees[i]-1,degrees[i]-1,self.numerator, alpha_d, root)
				self.querys.append("d^%d/dz^%d(%s)/(%s) at z = %s" % (degrees[i]-1,degrees[i]-1,self.numerator, alpha_d, root))
			i += 1
		self.set_requests(self.app_id)
		super(IntegralCauchyFormula,self).run()
		results = []
		for wfr in self.wolfram_request:
			for pod in wfr.get_pod():
				self.value += "\n%s\n" % pod.title
				for subpod in pod.subpods:
					self.value += "%s\n%s\n" % (subpod.text, subpod.img.attrib['src'])
					if pod.title == 'Result':
						results.append(subpod.text)
		self.reset_querys()
		query = ""
		i = 0
		operator = '+'
		if len(results) > 1:
			for result in results:
				if i == 0:
					operator = '('
				else:
					operator = ' + ('
				query += operator + result + ')'
				i += 1
		self.querys.append(query)
		self.set_requests(self.app_id)
		super(IntegralCauchyFormula,self).run()
		for wr in self.wolfram_request:		
			for pod in wr.get_pod():
				if pod.title == 'Result':
					self.value += '\nFinal Result: %s = %s\n%s\n' % (query,pod.text,pod.img.attrib['src'])
		

	def run (self):
		super(IntegralCauchyFormula,self).run()
		sols = ['Complex solutions', 'Real solutions', 'Complex solution', 'Real solution']
		splited_n = self.wolfram_request[0].get_pod()[0].text.split(' (')
		z = 1
		if (len(splited_n) % 2 == 0):
			z = 0
		for i in range(len(splited_n)-z):
			if i == 0:
				splited_n[i] += ''
			else:
				splited_n[i] = '(' + splited_n[i] + ')'
		if (len(splited_n) % 2 == 0):
			splited_n[-1] = '(' + splited_n[-1]
		for pod in self.wolfram_request[0].get_pod():
			if pod.title in sols:
				self.value += "\n%s\n" % pod.title
				for subpod in pod.subpods:
					self.roots.append(subpod.text.split(' = ')[1])
					self.value += "%s\n%s\n" % (subpod.text, subpod.img.attrib['src'])
		#self.roots = list(reversed(self.roots))
		self.extra_runs(splited_n)
		#self.value = self.wolfram_request[0].get_pod()[4].text
		self.answer = True



class DerivativePoint(BaseAced):
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
		super(DerivativePoint,self).run()
		self.value = self.wolfram_request[0].get_pod()[1].text
		self.answer = True


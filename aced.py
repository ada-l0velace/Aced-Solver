# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from sympy import sympify, Derivative, symbols, init_printing, pprint, Matrix, I, simplify, Integral, assume, var, Symbol, conjugate, Function, Q, pretty, degree, sqf, solve, fraction, re, im, oo
from w_requests import SymPyRequests
from prettytable import PrettyTable
import unicodedata
from sympy.calculus.singularities import singularities
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, convert_xor, auto_number, rationalize
transformations = (standard_transformations +(implicit_multiplication_application,convert_xor, rationalize,))
x, y, z = symbols('x y z')
var('A:D')
t = symbols('t', real=True)
init_printing(use_unicode=True)
from sympy import limit, Limit, Eq, apart, pi, N
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
	sympy_request = []

	def set_requests(self):
		self.sympy_request = []
		for query in self.querys:
			self.sympy_request.append(SymPyRequests())

	def parse_expression(self, expression):
		return parse_expr(expression, transformations = transformations)
	
	@abstractmethod
	def run (self):
		i = 0
		#for query,function in self.querys.iteritems():
		
		for query in self.querys:
			#print "Calculating:"
			#pprint (self._class(query[0], *query[1]), use_unicode=True)
			self.sympy_request[i].run(query = query[0], function= query[1], args= query[2])
			i += 1
		for r in self.sympy_request:
			r.join()


class Holomorph(BaseAced):
	"""
	Checks if a function is Holomorph
	"""

	def __init__(self, real, imaginary):
		
		self.func = "(%s) + (%s)i" % (real, imaginary)
		self.real = self.parse_expression(real)
		self.imaginary = self.parse_expression(imaginary)
		self.dudx = Derivative(self.real,x,1)
		self.dudy = Derivative(self.real,y,1)
		self.dvdx = Derivative(self.imaginary,x,1)
		self.dvdy = Derivative(self.imaginary,y,1)
		self.querys = [[self.dudx, self.dudx.doit, []], [self.dudy, self.dudy.doit, []], [self.dvdx, self.dvdx.doit, []], [self.dvdy, self.dvdy.doit, []]]
		self.matrix = None
		self.order = 1
		self.set_requests()
		self.answer = False
	
	def __str__(self):
		if(self.answer):
			print bcolors.BOLD
			pprint(self.matrix,use_unicode = True)
			print bcolors.ENDC
			print ""
			print bcolors.OKGREEN+ pretty(self.real+self.imaginary*I, use_unicode=True) +bcolors.ENDC
			return "\n"
		pprint(self.matrix,use_unicode = True)
		print ""
		print bcolors.FAIL + pretty(self.real+self.imaginary*I, use_unicode=True) +bcolors.ENDC
		return "\n"

	def run (self):
		super(Holomorph,self).run()
		dudx = self.sympy_request[0].response
		dudy = self.sympy_request[1].response
		dvdx = self.sympy_request[2].response
		dvdy = self.sympy_request[3].response
		self.matrix = Matrix([ [dudx, dudy], [dvdx, dvdy]])
		self.answer = (dudx == dvdy and dvdx == -dudy)
		

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

	def __init__(self, func, path, irange):
		self.func = self.parse_expression(func)		
		self.path = self.parse_expression(path)
		self.t =  self.func
		#self.t(t) = self.func
		self.dt = Derivative(self.path, symbols('t'), 1)		
		self.querys = [[self.dt , self.dt.doit, []], [self.t, self.t.subs, [z,self.path.replace('t', symbols('t',real=True))]]]
		self.range = irange
		self.set_requests()
		self.answer = False
		self.value = ""

	def __str__(self):
		if(self.answer):
			print bcolors.BOLD + pretty(self.query, use_unicode=True) + ' = ' + bcolors.ENDC + bcolors.OKGREEN + pretty(self.value, use_unicode=True) + bcolors.ENDC
			return ""
		return ""
		
	def run (self):
		super(PathIntegral,self).run()
		self.query = Integral (self.sympy_request[0].response.replace('t', symbols('t',real=True)) * self.sympy_request[1].response, self.range)
		self.value = self.query.doit()
		self.answer = True
		
class SingularitiesClassification(BaseAced):
	"""
	"""

	def __init__(self, func):
		self.func = self.parse_expression(func)
		self.numerator = fraction(self.func)[0]
		self.denominator = fraction(self.func)[1]
		self.singularities = solve(self.denominator, z)
		self.querys = []
		self.factors = []
		self.limits_e = []
		self.limits_a = []
		self.degrees = []
		self.singularity_l = []
		for singularity in self.singularities:
			self.factors.append(z - singularity)
		i = 0
		self.limit = 0
		for factor in self.factors:
			v = 0
			self.limit = 0
			while True:
				self.limit = limit(factor**v * self.func, z, self.singularities[i])
				if self.limit == 0:
					v -= 1
				elif self.limit == oo:
					v += 1
				else:
					self.limits_e.append((Limit(parse_expr(str(factor**v)+" * "+ str(self.func), evaluate=False), z, self.singularities[i])))
					self.limits_a.append(self.limit)
					self.degrees.append(v)
					self.singularity_l.append(self.singularities[i])
					break

			i += 1

	def __str__(self):
		for i in range(len(self.limits_e)):
			print bcolors.BOLD
			print pretty(Eq(self.limits_e[i],self.limits_a[i]))
			print bcolors.ENDC
			print bcolors.OKGREEN
			if self.degrees[i] == 0:
				self.degrees[i] = '0 (removable)'
			print "The singularity %s has order %s" % (pretty(self.singularity_l[i]),pretty(self.degrees[i])) 
			print bcolors.ENDC
			print bcolors.ENDC
				
		return ""
	def run (self):
		super(SingularitiesClassification,self).run()

class IntegralCauchyFormula(BaseAced):
	"""
	Calculates a integral with cauchy formula
	"""

	def __init__(self, numerator, denominator, center, ray, semi_circle = False, constant = 1/(2*pi *I)):
		#"d/dz(-(2i-2)(z-3i-4)^(3)+(3i-1)z^(2)) at z =2i+5"
		self.constant = constant
		self.semi_circle = semi_circle
		self.center = self.parse_expression(center)
		self.ray = self.parse_expression(ray)
		self.denominator =  self.parse_expression(denominator)
		self.save_den = self.parse_expression(denominator)
		self.denominators = str(self.denominator).split(')*(')
		self.numerator =  self.parse_expression(numerator)
		self.singularities = solve(self.denominator, z)
		self.denominators_aux = []
		self.factors = []
		self.querys = []
		self.infor = False
		for i in range(len(self.denominators)):
			if  ")**" in str(self.parse_expression(self.miss_par(self.denominators[i]))):
				self.infor = True
				self.denominators_aux.append(self.parse_expression(self.miss_par(self.denominators[i])))
		self.denominator = self.parse_expression('1') 
		self.denominators = self.denominators_aux
		for singularity in self.singularities:
			if not self.if_zero(singularity):
				self.factors.append(z - singularity)
				self.denominator *= (z - singularity)
		if self.infor:
			self.factors += self.denominators
		i = 0
		si = 0
		for singularity in self.singularities:
			if self.inside_circunferences(singularity, self.semi_circle):
				si += 1
		for singularity in self.singularities:
			if self.inside_circunferences(singularity, self.semi_circle): 
				if len(self.singularities) > si:
					function = self.numerator / self.denominator.replace(self.factors[i],1)
				else:
					function = self.numerator / self.save_den.replace(self.factors[i],1)
				#print pretty(function), '|', pretty(self.factors[i]), '|', singularity
				a = [function, Derivative(function,z,degree(self.factors[i])-1).doit().subs, [z,singularity]]
				self.querys.append(a)
			i += 1
		self.set_requests()
		self.answer = False
		self.value = ""

	def __str__(self):
		if(self.answer):
			print bcolors.BOLD
			print pretty (Integral(self.numerator / self.save_den, [z, Function('|%s| = %s' % (str(z - self.center), str(self.ray))), oo]))
			print bcolors.ENDC
			print '\nResult: '
			print bcolors.OKGREEN
			print bcolors.BOLD
			print pretty(self.value)
			print bcolors.ENDC
			print bcolors.ENDC
			return "" 
		return "An error ocurred"

	def miss_par(self, expr):
		#print expr[-3:-1] 
		if expr[0] != '(':
			if expr[0] == ')':
				expr[0] = ''
			expr = '(' + expr
		if expr[-3:-1] != '**':
			if expr[-1] != ')':
				expr = expr + ')'
		#print expr
		return expr
	
	def if_zero(self, singularity):
		if self.infor:
			for den in self.denominators:
				if den.subs(z, singularity) == 0:
					return True

		return False

	def inside_circunferences(self, singularity, semi_circle):
		if semi_circle and im(singularity) < 0:
			return False
		#print singularity
		#print (re(singularity) - re(self.center))**2, (im(singularity) - im(self.center))**2, self.ray ** 2
		#print (re(singularity) - re(self.center))**2 + (im(singularity) - im(self.center))**2 < self.ray ** 2
		return (re(singularity) - re(self.center))**2 + (im(singularity) - im(self.center))**2 < self.ray ** 2

	def run (self):
		super(IntegralCauchyFormula,self).run()
		self.value = self.parse_expression('0') 
		
		for sr in self.sympy_request:
			#print sr.response
			#print simplify(sr.response)
			self.value += sr.response
		self.value = self.constant * simplify(self.value) * 2*pi*I
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

class PartialFractions(BaseAced):
	"""
	"""

	def __init__(self, func):
		self.func = self.parse_expression(func)
		self.querys = []
		print pretty(apart(self.func))
	
	def run (self):
		super(PartialFractions,self).run()
		
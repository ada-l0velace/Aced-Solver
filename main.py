from aced import Holomorph, SimpleOperation, PathIntegral, DerivativePoint, IntegralCauchyFormula, SingularitiesClassification
from aced import PartialFractions
from w_requests import AcedSolverRequests
from sympy import Symbol, symbols, init_printing, pi, oo

x, y, z = symbols('x y z')
t = Symbol('t', real=True)
init_printing(use_unicode=True)

if __name__ == "__main__":
	# acedDP0 = Holomorph('5cos(x)E^(-y)+5y','-5E^(-y)sin(x)-5x')  
	# acedDP1 = Holomorph('-5cos(x)E^(-y)+5E^(x)sin(y)', '-5cos(y)E^(x)-5E^(-y)sin(x)')
	# acedDP2 = Holomorph('-9x^(2)y+3y^(3)+4x*cos(y)E^(x)-4y*E^(x)sin(y)','3*x^(3)-9*xy^(2)+4*y*cos(y)*E^(x)+4*x*E^(x)sin(y)')
	# acedDP3 = Holomorph('(4x*cos(x)*E^(-y)-4y*E^(-y)sin(x)-x^(2)+y^(2))','-4*y*cos(x)*E^(-y)-4*x*E^(-y)*sin(x)-2*xy')
	
	# acedDP4 = Holomorph('-2x^(2)+2y^(2) + 4x','4xy + 4y')  
	# acedDP5 = Holomorph('4x*cos(y)*E^(x) - 4y*E^(x)*sin(y) - 4cos(-y)*E^(x)', '4y*cos(y)*E^(x) + 4x*E^(x)*sin(y)-4*E^(x)*sin(-y)')
	# acedDP6 = Holomorph('-12x^(2)y + 4y^(3) + 4 cos(x)*E^(-y)','4x^(3) - 12xy^(2) + 4E^(-y)*sin(x)')
	# acedDP7 = Holomorph('-5y*cos(x)* E^(y) + 5x*E^(y)*sin(x) - 5cos(x)*E^(y)','5*x*cos(x)*E^(y) + 5*y*E^(y)*sin(x) + 5*E^(y)*sin(x)')
	# acedDP8 = Holomorph('-2y^(3) + 6*x^(2)*y + 3x','-2x^(3) + 6xy^(2) + 3y-3')
	# acedDP9 = Holomorph('3x^(3) - 9xy^(2) - 2x^(2)+2y^(2)','-4xy + 9x^(2)*y - 3y^(3)')
	# #acedSF = SimpleOperation('series representations (1/((w+i+3)-(-4i-2)))')
	# acedPI = PathIntegral('conjugate(z)', '-(3I-2)t^(2)-(3I-1)t-I-2', (t,-2,1))
	# #acedDP = DerivativePoint('-(2i-2)(z-3i-4)^(3)+(3i-1)z^(2)', '2i+5')
	# acedICF0 = IntegralCauchyFormula('5z^(2)-2Iz', '(z^(2)+4z+5)(z+2)','-2I-1','2')
	# acedICF1 = IntegralCauchyFormula('-z^(2)-3z','(z+3I+1)^(2)(z+3I)','-3I-1', '4')
	# acedICF2 = IntegralCauchyFormula('z+5I','(z+2I)(z-2I)(z-1)','3I-1', '2')
	# acedICF3 = IntegralCauchyFormula('(2I+2)z^(2) - (4I-4)z','z+4I-1','0', '5')
	# acedICF4 = IntegralCauchyFormula('(-3Iz^(2)-4z)','(z^(2)+8z+17)(z+3)','-3I-2', '4')
	# acedICF5 = IntegralCauchyFormula('(3Iz^(2)+5Iz)','(z+I)(z+I-1)^(2)','-4I+3', '4')
	# acedICF6 = IntegralCauchyFormula('(2I-4)z^(2)-(2I-3)z+I+2','(z+3I+3)^(2)','0', '5')
	# acedICF7 = IntegralCauchyFormula('-4z^(2)-(2I+3)z+e^(pi*I)','z+I','0', '5')
	# acedICF8 = IntegralCauchyFormula('-4Iz+5I','(z+1)(z-I-1)(z-I+2)','2I-3', '2')
	# acedICF9 = IntegralCauchyFormula('2I*z^(2)-4z','(z^(2)+1)(z-1)','3I-1', '4')
	# acedICF10 = IntegralCauchyFormula('-3I*z^(2)+3I*z','(z+I+1)^(2)*(z+I)','-2', '4')
	# acedICF11 = IntegralCauchyFormula('2z^(2) + 3I*z','(z^(2) + 2Iz +4z + 4I +2)(z+2)','-I-5', '3')
	# acedICF12 = IntegralCauchyFormula('2z^(2) + 3z','(z-I-2)^(2)*(z-2)','I+1', '2')
	# acedICF13 = IntegralCauchyFormula('4Iz-2I','(z + I + 3)(z + 3)(z-2I+3)','-2I-2','2')
	# acedICF14 = IntegralCauchyFormula('2*z-3','(z + 2)(z +2I+1)(z-2I+1)','-I+1','3')
	# acedICF15 = IntegralCauchyFormula('(4z^(2)+9z+4)','(z^(2)+4z+5)(z^(2)+2z+2)','0', 'oo', True, 5/pi)
	acedICF16 = IntegralCauchyFormula('(2z^(2)-18z+41)','(z^(2)-4z+5)(z^(2)-6z+10)','0', 'oo', True, 5/pi)
	# acedICF17 = IntegralCauchyFormula('(4z^(2)-18z+21)','(z^(2)-2z+2)(z^(2)-4z+5)','0', 'oo', True, 5/pi)
	
	# acedYolo = SingularitiesClassification('(z^(2) + 5z + 4) / ((z+4)*(z+1)^3)')
	# acedYolo1 = SingularitiesClassification('(z^(2)-8Iz-15) / ((z-3I)(z-5I)^(3))')
	# #acedPF = PartialFractions("(3I-2)/((2z+7I-6)((z+3I-3)^(4)))")
	# aPI = [acedPI]
	# aux = [acedDP0, acedDP1, acedDP2, acedDP3]
	# aux2 = [acedDP4, acedDP5, acedDP6, acedDP7, acedICF8]
	# aux3 = [acedICF0, acedICF1, acedICF2, acedICF3, acedICF4, acedICF5, acedICF6, acedICF7, acedICF8, acedICF9, acedICF10, acedICF11]
	# all_l = aPI + aux + aux2 + aux3
	ASR = AcedSolverRequests([acedICF16])
	ASR.run()

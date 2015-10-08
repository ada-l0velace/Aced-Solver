from aced import Holomorph, SimpleOperation, PathIntegral, DerivativePoint, IntegralCauchyFormula
from w_requests import AcedSolverRequests

APP_ID = '#'

if __name__ == "__main__":
	#acedH = Holomorph('e^(x)cos(y)+ie^(x)sin(y)', APP_ID)
	#acedH.run()
	#print acedH
	acedDP0 = Holomorph('5cos(x)e^(-y)+5y','-5e^(-y)sin(x)-5x', APP_ID)  
	acedDP1 = Holomorph('-5cos(x)e^(-y)+5e^(x)sin(y)', '-5cos(y)e^(x)-5e^(-y)sin(x)', APP_ID)
	acedDP2 = Holomorph('-9x^(2)y+3y^(3)+4x*cos(y)e^(x)-4y*e^(x)sin(y)','3*x^(3)-9*xy^(2)+4*y*cos(y)*e^(x)+4*x*e^(x)sin(y)', APP_ID)
	acedDP3 = Holomorph('(4x*cos(x)*e^(-y)-4y*e^(-y)sin(x)-x^(2)+y^(2))','-4*y*cos(x)*e^(-y)-4*x*e^(-y)*sin(x)-2*xy', APP_ID)
	
	acedDP4 = Holomorph('-2x^(2)+2y^(2) + 4x','4xy + 4y', APP_ID)  
	acedDP5 = Holomorph('4x*cos(y)*e^(x) - 4y*e^(x)*sin(y) - 4cos(-y)*e^(x)', '4y*cos(y)*e^(x) + 4x*e^(x)*sin(y)-4*e^(x)*sin(-y)', APP_ID)
	acedDP6 = Holomorph('-12x^(2)y + 4y^(3) + 4 cos(x)*e^(-y)','4x^(3) - 12xy^(2) + 4e^(-y)*sin(x)', APP_ID)
	acedDP7 = Holomorph('-5y*cos(x)* e^(y) + 5x*e^(y)*sin(x) - 5cos(x)*e^(y)','5*x*cos(x)*e^(y) + 5*y*e^(y)*sin(x) + 5*e^(y)*sin(x)', APP_ID)
	

	acedSF = SimpleOperation('series representations (1/((w+i+3)-(-4i-2)))', APP_ID)
	acedPI = PathIntegral('conjugate(z)', '-(3i-2)t^(2)-(3i-1)t-i-2', [-2,1], APP_ID)
	acedPI1 = PathIntegral('conjugate(z)', '-(3i-2)t^(2)-(3i-1)t-i-2', [-2,1], APP_ID)
	acedDP = DerivativePoint('-(2i-2)(z-3i-4)^(3)+(3i-1)z^(2)', '2i+5', APP_ID)
	acedICF0 = IntegralCauchyFormula('5z^(2)-2iz', '(z^(2)+4z+5)(z+2)','-2i-1','2', APP_ID)
	acedICF1 = IntegralCauchyFormula('-z^(2)-3z','(z+3i+1)^(2)(z+3i)','-3i-1', '4', APP_ID)
	acedICF2 = IntegralCauchyFormula('z+5i','(z+2i)(z-2i)(z-1)','3i-1', '2', APP_ID)
	acedICF3 = IntegralCauchyFormula('(2i+2)z^(2) - (4i-4)z','z+4i-1','0', '5', APP_ID)
	acedICF4 = IntegralCauchyFormula('(-3iz^(2)-4z)','(z^(2)+8z+17)(z+3)','-3i-2', '4', APP_ID)
	acedICF5 = IntegralCauchyFormula('(3iz^(2)+5iz)','(z+i)(z+i-1)^(2)','-4i+3', '4', APP_ID)
	
	aux = [acedDP0, acedDP1, acedDP2, acedDP3]
	aux2 = [acedDP4, acedDP5, acedDP6, acedDP7]
	aux3 = [acedICF0, acedICF1, acedICF2, acedICF3, acedICF4, acedICF5]
	ASR = AcedSolverRequests(aux)
	ASR.run()
	#acedDP0.run()
	#acedDP1.run()
	#acedDP2.run()
	#acedDP3.run()
	#print acedDP0
	#print '---------------------------'
	#print acedDP1
	#print '---------------------------'
	#print acedDP2
	#print '---------------------------'
	#print acedDP3
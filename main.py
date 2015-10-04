from aced import Holomorph, SimpleOperation, PathIntegral, DerevativePoint, IntegralCauchyFormula

APP_ID = '#'

if __name__ == "__main__":
	acedH = Holomorph('e^(x)cos(y)+ie^(x)sin(y)', APP_ID)
	#acedH.run()
	#print acedH
	acedSF = SimpleOperation('series representations (1/((w+i+3)-(-4i-2)))', APP_ID)
	acedPI = PathIntegral('conjugate(z)', '-(3i-2)t^(2)-(3i-1)t-i-2', [-2,1], APP_ID)
	acedDP = DerevativePoint('-(2i-2)(z-3i-4)^(3)+(3i-1)z^(2)', '2i+5', APP_ID)
	acedICF = IntegralCauchyFormula('(2i-4)z^2-(2i-3)z+i+2', '(z+3i+3)^2', APP_ID)
	acedICF.run()

	print acedICF
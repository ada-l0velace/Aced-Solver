from aced import Holomorph, SimpleOperation, PathIntegral

APP_ID = '#'

if __name__ == "__main__":
	acedH = Holomorph('e^(x)cos(y)+ie^(x)sin(y)', APP_ID)
	#acedH.run()
	#print acedH
	acedSF = SimpleOperation('series representations (1/((w+i+3)-(-4i-2)))', APP_ID)
	acedPI = PathIntegral('conjugate(z)', '-(3i-2)t^(2)-(3i-1)t-i-2', [-2,1], APP_ID)
	acedPI.run()
	print acedPI
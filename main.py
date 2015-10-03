from aced import Holomorph

APP_ID = '#'

if __name__ == "__main__":
	acedH = Holomorph('e^(x)cos(y)+ie^(x)sin(y)', APP_ID)
	acedH.run()
	print acedH
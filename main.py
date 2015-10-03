from aced import Holomorph

APP_ID = 'GA7EVL-J837G239J9'

if __name__ == "__main__":
	acedH = Holomorph('e^(x)cos(y)+ie^(x)sin(y)', APP_ID)
	acedH.run()
	print acedH
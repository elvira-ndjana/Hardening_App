import base64

def encodage():
	file = open("29-05-2022 à 16h04m49s.csv", "r")
	data = file.read()
	print(data)
	encoded = base64.b64encode(data.encode())
	file.close()
	return "29-05-2022 à 16h04m49s.csv", encoded

nom, end = encodage()
print(nom)
print(end)
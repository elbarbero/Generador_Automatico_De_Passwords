import encriptacion as enc

class Contrasena():

	def __init__(self, ident, web, username, password):
		self.id = ident
		self.web = web
		self.username = username
		self.password = password

	def __str__(self):
		return "Contraseña del usuario {} para el sitio web {} y la contraseña {}".format(self.username, self.web, self.password)


#c = Contrasena(1, "12345Ral", 2)
#print(c.password)
#print(c.s.decrypt(c.s.key, c.password))


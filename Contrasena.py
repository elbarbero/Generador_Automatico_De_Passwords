import encriptacion as enc
class Contrasena():

	def __init__(self, ident, password, username, web):
		self.s = enc.Seguridad()
		self.id = ident
		self.password = self.s.encrypt(self.s.key, str(password))
		self.username = username
		self.web = web

	def __str__(self):
		return "Contraseña del usuario {}".format(self.user.nick)


#c = Contrasena(1, "12345Ral", 2)
#print(c.password)
#print(c.s.decrypt(c.s.key, c.password))


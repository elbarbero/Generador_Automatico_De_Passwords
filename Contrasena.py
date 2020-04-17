import hashlib

class Contrasena():

	def __init__(self, ident, password, user):
		self.id = ident
		self.password = self.encrypt(password)
		self.user = user

	def __str__(self):
		return "Contraseña del usuario {}".format(self.user.nick)

	def encrypt(self, data):
		h = hashlib.new("sha256", str(data).encode())

		return h.digest(), h.hexdigest()
 
	def decrypt(self):
		pass


#c = Contrasena(1, "12345Ral", 2)
#print(c.encrypt(str(c.password)))
#print(c.decrypt())